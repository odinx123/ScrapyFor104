import json
import opencc

if __name__ == '__main__':
    # # 讀取 JSON 文件
    # with open('test.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)

    # converter = opencc.OpenCC('s2t.json')
    # # 列出所有的 title
    # for item in data:
    #     title = item.get('title')  # 使用 get() 方法以防止 key 不存在時引發錯誤
    #     print(f'Before:{title}, After:{converter.convert(title)}')
    from datetime import datetime

    # 原始日期字串
    my_date = '5/10'

    # 將日期字串轉換為 datetime 物件，假設當前年份為2024
    date_obj = datetime.strptime(my_date, "%m/%d").replace(year=datetime.now().year)

    # 格式化日期為 "yyyy/mm/dd" 格式
    # formatted_date = date_obj.strftime("%Y/%m/%d")

    print("轉換後的日期 (yyyy/mm/dd):", date_obj)




