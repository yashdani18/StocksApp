import pprint

import pymongo as pymongo
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tabulate import tabulate

client = pymongo.MongoClient("")
# print(db)
db = client['op_db']

collection_posts = db['collection_posts']
# post = {
#     'Author': 'Phil',
#     'Book': 'Shoe Dog'
# }
# post_id = collection_posts.insert_one(post).inserted_id
# print(collection_posts.find_one())

collection_jobs = db['collection_jobs']

# myQuery = {'name': 'Akuna Capital'}
# collection_jobs.delete_one(myQuery)
# myQuery = {'name': 'Volvo'}
# collection_jobs.delete_one(myQuery)
# myQuery = {'name': 'Two Sigma'}
# collection_jobs.delete_one(myQuery)
# myQuery = {'name': 'Lockheed Martin'}
# collection_jobs.delete_one(myQuery)
# myQuery = {'name': 'Mastercard'}
# collection_jobs.delete_one(myQuery)
# myQuery = {'name': 'Microsoft'}
# collection_jobs.delete_one(myQuery)


def print_dataframe(p_dataframe):
    print(tabulate(p_dataframe, headers="keys", tablefmt="psql"))


def insert_initial():
    url = 'https://github.com/pittcsc/Summer2023-Internships'

    response = requests.get(url).text

    soup = BeautifulSoup(response, 'lxml')

    rows = soup.find('tbody').find_all('tr')
    print(len(rows))
    len_jobs = len(rows)

    name = []
    location = []
    notes = []

    jobs = []
    for row in rows:
        columns = row.find_all_next('td')
        company_name = columns[0]
        if company_name.find('a'):
            val_name = company_name.find('a').text
            name.append(val_name)
        else:
            val_name = company_name.text
            name.append(val_name)

        val_location = columns[1].text
        val_notes = columns[2].text
        location.append(val_location)
        notes.append(val_notes)
        dict_job = {
            'name': val_name,
            'location': val_location,
            'notes': val_notes
        }
        jobs.append(dict_job)

    pprint.pprint(jobs)

    result = collection_jobs.insert_many(jobs)
    if len(result.inserted_ids) == len_jobs:
        print('Insert successful')
    else:
        print('Insert failed')

    df = pd.DataFrame(list(zip(name, location, notes)))
    df.columns = ['Name', 'Location', 'Notes']
    print_dataframe(df)
    return df


# insert_initial()


def get_all_jobs_from_github():
    url = 'https://github.com/pittcsc/Summer2023-Internships'

    response = requests.get(url).text

    soup = BeautifulSoup(response, 'lxml')

    rows = soup.find('tbody').find_all('tr')
    print(len(rows))
    len_jobs = len(rows)

    name = []
    location = []
    notes = []

    jobs_from_github = []
    for row in rows:
        columns = row.find_all_next('td')
        company_name = columns[0]
        if company_name.find('a'):
            val_name = company_name.find('a').text
            name.append(val_name)
        else:
            val_name = company_name.text
            name.append(val_name)

        val_location = columns[1].text
        val_notes = columns[2].text
        location.append(val_location)
        notes.append(val_notes)
        dict_job = {
            'name': val_name,
            'location': val_location,
            'notes': val_notes
        }
        jobs_from_github.append(dict_job)

    # pprint.pprint(jobs_from_github)
    return jobs_from_github


# get_all_jobs_from_github()


def get_all_jobs_from_db():
    jobs_from_db = collection_jobs.find().sort('name')
    # print(len(jobs_from_db))
    # for job in jobs_from_db:
    #     print(job['name'])
    return jobs_from_db


# get_all_jobs_from_db()


def delete_all_documents_from_collection(collection):
    result = collection.delete_many({})
    print(result.deleted_count, 'documents deleted')


# delete_all_documents_from_collection(collection_jobs)


def get_count_of_documents_from_collection():
    return collection_jobs.count_documents({})


# print(get_count_of_documents_from_collection())


def insert_documents_into_collection_jobs(jobs):
    len_job = len(jobs)
    if len_job == 0:
        return 'No records to insert'
    result = collection_jobs.insert_many(jobs)
    if len(result.inserted_ids) == len_job:
        return 'Records inserted successfully'
    else:
        return 'Records insertion failed'
