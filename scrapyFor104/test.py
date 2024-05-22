import json
import opencc
import pprint

def extract_job_cat_nos(data):
    no_list = []
    if isinstance(data, dict):
        if 'no' in data:
            no_list.append(data['no'])
        if 'n' in data:
            for item in data['n']:
                no_list.extend(extract_job_cat_nos(item))
    elif isinstance(data, list):
        for item in data:
            no_list.extend(extract_job_cat_nos(item))
    return no_list

if __name__ == '__main__':
    # # 讀取 JSON 文件
    # with open('test.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)

    # converter = opencc.OpenCC('s2t.json')
    # # 列出所有的 title
    # for item in data:
    #     title = item.get('title')  # 使用 get() 方法以防止 key 不存在時引發錯誤
    #     print(f'Before:{title}, After:{converter.convert(title)}')
    with open('category.json', 'r', encoding='utf-8') as file:
        job_cat_data = json.load(file)

    # for job_cat in job_cat_data:
    # print(job_cat_data[0]['n'][1]['n'][0]['no'])

    ans = extract_job_cat_nos(job_cat_data)

    print(ans)
    # for job_cat in job_cat_data:
    #     for job0 in job_cat['n']:
    #         for job1 in job0:
    #             for job2 in job1['n']:
    #                 for job3 in job2:
    #                     print(job3['no'], end=' ')
        # for job in job_cat['n']:
        #     print(job)




