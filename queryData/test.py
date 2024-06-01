from jobQuery.jobAPI import JobDatabase
import pprint
# from jobAPI import JobDatabase

def main():
    db = JobDatabase(
        host="save-job-data.mysql.database.azure.com",
        username="azureruser",
        password="@C110152318",
        database="job104"
    )

    print('=============================================')
    # print(db.get_number_by_filter(category=None,
    #                              skill=None,
    #                              education=None,
    #                              tool=['python'],
    #                              experience=None,
    #                              days=None,
    #                              min_salary=None,
    #                              max_salary=None))
    tool = db.get_all_tools()
    for t in tool:
        print(db.get_number_by_filter(category=None,
                                 skill=None,
                                 education=None,
                                 tool=[t],
                                 experience=None,
                                 days=None,
                                 min_salary=None,
                                 max_salary=None))
    

if __name__ == '__main__':
    main()