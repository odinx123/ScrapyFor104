from selenium import webdriver
from time import sleep
import json

if __name__ == '__main__':
    scroll_time = int(input('請輸入想要捲動幾次'))
    driver = webdriver.Chrome()
    driver.get('https://www.dcard.tw/f')
    results = []
    prev_ele = None
    for now_time in range(1, scroll_time+1):
        sleep(2)
        eles = driver.find_elements_by_class_name('tgn9uw-0')
        # 若串列中存在上一次的最後一個元素，則擷取上一次的最後一個元素到當前最後一個元素進行爬取
        try:
            # print(eles)
            # print(prev_ele)
            eles = eles[eles.index(prev_ele):]
        except:
            pass
        for ele in eles:
            try:
                title = ele.find_element_by_class_name('tgn9uw-3').text
                href = ele.find_element_by_class_name(
                    'tgn9uw-3').get_attribute('href')
                subtitle = ele.find_element_by_class_name('tgn9uw-4').text
                result = {
                    'title': title,
                    'href': href,
                    'subtitle': subtitle
                }
                results.append(result)
            except:
                pass
        prev_ele = eles[-1]
        print(f"now scroll {now_time}/{scroll_time}")
        js = "window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(js)
    with open('Dcard-articles.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2,
                  sort_keys=True, ensure_ascii=False)
    driver.quit()