import json
import os
import re
from pathlib import Path
from urllib.parse import urlencode, urlparse

import scrapy

from scrapyFor104.items import Scrapyfor104Item


class Crawljob104Spider(scrapy.Spider):
    name = "crawlJob104"

    search_api = "https://www.104.com.tw/jobs/search/api/jobs"
    detail_api = "https://www.104.com.tw/job/ajax/content/{job_id}"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.104.com.tw/jobs/search/",
    }

    async def start(self):
        for request in self.build_start_requests():
            yield request

    def build_start_requests(self):
        category_file = Path(__file__).resolve().parents[2] / "category.json"
        with category_file.open("r", encoding="utf-8") as file:
            job_cat_data = json.load(file)

        start_page = int(os.getenv("SCRAPY104_START_PAGE", "1"))
        end_page = int(os.getenv("SCRAPY104_END_PAGE", "2"))
        jobcat_prefix = os.getenv("SCRAPY104_JOBCAT_PREFIX", "2007")

        for jobcat in self.extract_job_cat_nos(job_cat_data):
            if not jobcat.startswith(jobcat_prefix):
                continue

            for page in range(start_page, end_page + 1):
                query = urlencode(
                    {
                        "jobcat": jobcat,
                        "page": page,
                        "jobsource": "2018indexpoc",
                        "mode": "s",
                    }
                )
                yield scrapy.Request(
                    url=f"{self.search_api}?{query}",
                    headers=self.headers,
                    callback=self.parse_search,
                    meta={"jobcat": jobcat, "page": page},
                )

    def extract_job_cat_nos(self, data):
        no_list = []
        if isinstance(data, dict):
            if "n" in data:
                for item in data["n"]:
                    no_list.extend(self.extract_job_cat_nos(item))
            elif "no" in data:
                no_list.append(data["no"])
        elif isinstance(data, list):
            for item in data:
                no_list.extend(self.extract_job_cat_nos(item))
        return no_list

    def parse_search(self, response):
        try:
            payload = json.loads(response.text)
        except json.JSONDecodeError as exc:
            self.logger.warning("Search API returned non-JSON response: %s (%s)", response.url, exc)
            return

        jobs = payload.get("data") or []
        if not jobs:
            self.logger.info(
                "No jobs found for jobcat=%s page=%s",
                response.meta.get("jobcat"),
                response.meta.get("page"),
            )
            return

        for job in jobs:
            job_id = self.extract_job_id(job)
            if not job_id:
                self.logger.debug("Skipped search result without job id: %s", job)
                continue

            yield scrapy.Request(
                url=self.detail_api.format(job_id=job_id),
                headers={
                    **self.headers,
                    "Referer": f"https://www.104.com.tw/job/{job_id}",
                },
                callback=self.parse_every_job,
                meta={"job_id": job_id},
            )

    def extract_job_id(self, job):
        job_url = (job.get("link") or {}).get("job") or job.get("jobUrl") or ""
        match = re.search(r"/job/([^/?#]+)", urlparse(job_url).path)
        if match:
            return match.group(1)
        return None

    def parse_every_job(self, response):
        try:
            job_data = json.loads(response.text)["data"]
        except (json.JSONDecodeError, KeyError) as exc:
            self.logger.warning("Detail API parse failed: %s (%s)", response.url, exc)
            return

        header = job_data.get("header") or {}
        condition = job_data.get("condition") or {}
        detail = job_data.get("jobDetail") or {}

        item = Scrapyfor104Item()
        item["source_job_key"] = response.meta.get("job_id", "")
        item["source_url"] = f"https://www.104.com.tw/job/{response.meta.get('job_id', '')}"
        item["job_title"] = header.get("jobName", "")
        item["update_time"] = header.get("appearDate", "")
        item["company"] = header.get("custName", "")
        item["exp"] = condition.get("workExp", "")
        item["edu"] = self.split_education(condition.get("edu", ""))
        item["skill"] = [skill.get("description", "") for skill in condition.get("skill", [])]
        item["specialty_tool"] = [tool.get("description", "") for tool in condition.get("specialty", [])]
        item["category_name"] = [category.get("description", "") for category in detail.get("jobCategory", [])]
        item["salary"] = detail.get("salary", "")
        item["address"] = f"{detail.get('addressRegion', '')}{detail.get('addressDetail', '')}"
        item["industry"] = job_data.get("industry", "")

        yield item

    def split_education(self, education):
        if not education:
            return []
        return [value for value in education.split("、") if value]
