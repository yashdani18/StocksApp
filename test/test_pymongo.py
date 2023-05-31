from pymongo import MongoClient
import pprint

url = 'mongodb+srv://yashdani18:ForgotPassword01@cluster0.0wi48vj.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(url)

db = client['investment_manager']

print(db.list_collections().next())

collections = db.list_collection_names()

for collection in collections:
    print(collection)

collection_ticker = db['ticker']

stock = {
    'name': 'Sarda Energy',
    'ticker': 'SARDAEN',
    'price': 1000
}

if collection_ticker.find_one({'ticker': stock['ticker']}) is not None:
    print('record already exists')
else:
    print('record does not exist')
    if collection_ticker.insert_one(stock):
        print('data inserted')



pprint.pprint(collection_ticker.find_one({'ticker': 'SARDAE'}))

stocks = collection_ticker.find()
sardas = collection_ticker.find({'ticker': 'SARDAEN'})

for index, sarda in enumerate(sardas, start=2):
    print(index, sarda)

cursor = collection_ticker.aggregate(
    [
        {"$group": {"_id": "$ID", "unique_ids": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
        {"$match": {"count": { "$gte": 2 }}}
    ]
)

def print_all():
    istocks = collection_ticker.find()
    for istock in istocks:
        print(istock)


if collection_ticker.find_one({'ticker': stock['ticker']}):
    if collection_ticker.replace_one({'ticker': stock['ticker']}, stock).acknowledged:
        print('Document updated successfully')
    else:
        print('Document failed to update')
else:
    if collection_ticker.insert_one(stock).acknowledged:
        print('Document inserted successfully')
    else:
        print('Document failed to insert')

# for stock in stocks:
#     pprint.pprint(stock)


