import json
import opencc

if __name__ == '__main__':
    # # 讀取 JSON 文件
    with open('test.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    converter = opencc.OpenCC('s2t.json')
    # 列出所有的 title
    for item in data:
        title = item.get('title')  # 使用 get() 方法以防止 key 不存在時引發錯誤
        print(f'Before:{title}, After:{converter.convert(title)}')



