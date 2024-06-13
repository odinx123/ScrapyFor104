import pprint
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import sys
import os
# 獲取當前腳本所在目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
# 獲取上層目錄
parent_dir = os.path.dirname(current_dir)
# 將上層目錄添加到sys.path
sys.path.append(parent_dir)
# 現在可以導入上層目錄中的模組或包
from queryData.jobQuery import JobDatabase
import random

# 推薦函數
def recommend(job_id, cosine_sim, num_of_jobs=5):
    idx = jobs[jobs['job_id'] == job_id].index[0]  # 獲取工作的索引(dataframe的index)
    sim_scores = list(enumerate(cosine_sim[idx]))  # 獲取該工作的所有相似度
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_of_jobs*2]  # 取前5個相似的工作，0是自己
    job_indices = random.sample([i[0] for i in sim_scores], num_of_jobs)
    return [i for i in jobs['job_id'].iloc[job_indices]]

if __name__ == '__main__':
    db = JobDatabase(
        host="localhost",
        username="root",
        password="9879",
        database="jobDatabase"
    )

    jobs = db.get_jobInfo_by_filter(
        category=None,
        skill=None,
        education=None,
        tool=None,
        experience=None,
        days=None,
        min_salary=None,
        max_salary=None,
        limit=None,
    )
    jobs = [j for j in jobs]
    jobs = pd.DataFrame(jobs)

    # 將列表轉換為字符串
    jobs['category'] = jobs['category'].apply(lambda x: ' '.join(x))
    jobs['skill'] = jobs['skill'].apply(lambda x: ' '.join(x))
    jobs['tool'] = jobs['tool'].apply(lambda x: ' '.join(x))

    # 將類別、技能和工具合併為一個文本列
    jobs['combined'] = jobs['category'] + ' ' + jobs['skill'] + ' ' + jobs['tool']

    # 計算TF-IDF特徵
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(jobs['combined'])
    # print(tfidf.get_feature_names_out())

    # 計算餘弦相似度
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # 推薦相似的工作
    recommended_jobs = recommend(1367, cosine_sim)

    pprint.pprint(db.get_jobInfo_by_id(1367))
    print()

    for job_id in recommended_jobs:
        pprint.pprint(db.get_jobInfo_by_id(job_id))
