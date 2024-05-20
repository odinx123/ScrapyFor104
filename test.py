import requests
import json


def get_job(job_id):
    """取得職缺詳細資料"""
    url = f'https://www.104.com.tw/job/ajax/content/{job_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        'Referer': f'https://www.104.com.tw/job/{job_id}'
    }

    r = requests.get(url, headers=headers)
    if r.status_code != requests.codes.ok:
        print('請求失敗', r.status_code)
        return

    data = r.json()
    return data['data']

job_info = get_job('83ix3')
data = json.dumps(job_info, indent=4, ensure_ascii=False)
print(data)
