from get.get_jobs_root import get_all_jobs_from_db, get_all_jobs_from_github, insert_documents_into_collection_jobs


def get_all_new_jobs():
    jobs_from_db = get_all_jobs_from_db()
    jobs_from_github = get_all_jobs_from_github()
    jobs_from_github = sorted(jobs_from_github, key=lambda d: d['name'])
    new_jobs = []
    job_found_in_github = False
    index_github = 0
    for index, job_db in enumerate(jobs_from_db):
        print('outer loop', job_db)
        if job_db['name'] != jobs_from_github[index_github]['name']:
            new_jobs.append(jobs_from_github[index_github])
            index_github += 1
            while job_db['name'] != jobs_from_github[index_github]['name']:
                new_jobs.append(jobs_from_github[index_github])
                index_github += 1
            index_github += 1
        else:
            index_github += 1

    for index in range(index_github, len(jobs_from_github)):
        new_jobs.append(jobs_from_github[index])

    print(insert_documents_into_collection_jobs(new_jobs))
    for job in new_jobs:
        print(job['name'])

    dict_jobs = {
        'new_jobs': new_jobs,
        'all_jobs': jobs_from_github
    }
    return dict_jobs


# print(len(jobs_from_db))
# for index, job in enumerate(jobs_from_db):
#     print(index, job['name'])

# for job in jobs_from_github:
#     print(job['name'])

# jobs_from_db = [
#     {
#         'name': 'Akuna'
#     },
#     {
#         'name': 'IMC'
#     },
#     {
#         'name': 'Bridgewater'
#     },
#     {
#         'name': 'Citadel'
#     },
#     {
#         'name': 'Five Rings'
#     },
#     {
#         'name': 'Tower Capital'
#     }
# ]

# jobs_from_github = [
#     {
#         'name': 'Akuna'
#     },
#     {
#         'name': 'Paypal'
#     },
#     {
#         'name': 'IMC'
#     },
#     {
#         'name': 'Bridgewater'
#     },
#     {
#         'name': 'AngelList'
#     },
#     {
#         'name': 'AQR'
#     },
#     {
#         'name': 'Citadel'
#     },
#     {
#         'name': 'Five Rings'
#     },
#     {
#         'name': 'Tower Capital'
#     },
#     {
#         'name': 'Mastercard'
#     }
# ]

# jobs_from_github.sort()

# print(jobs_from_github)