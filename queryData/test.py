# from jobQuery.jobAPI import JobDatabase
import pprint
from jobAPI import JobDatabase

def main():
    db = JobDatabase(
        host="save-job-data.mysql.database.azure.com",
        username="azureruser",
        password="@C110152318",
        database="job104"
    )

    print('=============================================')
    print(db.get_number_by_filter(category=None,
                                 skill=None,
                                 education=None,
                                 tool=['python'],
                                 experience=None,
                                 days=None,
                                 min_salary=None,
                                 max_salary=None))

    jobs = db.get_jobInfo_by_filter(category=['後端工程師', '網路管理工程師'],
                                 skill=None,
                                 education=None,
                                 tool=None,
                                 experience=None,
                                 days=None,
                                 min_salary=None,
                                 max_salary=None
                                )
    
    # name = 'jobs'
    # with open(fr'{name}.txt', 'w', encoding='utf-8') as f:
    #     data = [j for j in jobs]
    #     pprint.pprint(data, stream=f)

    for i, j in enumerate(jobs):
        print(i)
        print(j)
        print('=============================================')
    # for job, j in enumerate(jobs):
    #     if job <= 10:
    #         break
    #     print(job)
    #     print('=============================================')

if __name__ == '__main__':
    main()