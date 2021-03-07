import requests
from firebase_admin import credentials, firestore, initialize_app
from apscheduler.schedulers.background import BackgroundScheduler

cred = credentials.Certificate('CONNECT-TO-FIREBASE')
default_app = initialize_app(cred)
db = firestore.client()
property_ref = db.collection('properties')


# if user searches for something not in the database
def search_database(city, state):
    url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"

    querystring = {"city": city,
                   "limit": "200",
                   "offset": "0",
                   "state_code": "GA",
                   "sort": "relevance"}

    headers = {
        'x-rapidapi-key': "YOUR-API-KEY",
        'x-rapidapi-host': "realtor.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    results = response.json()['properties']
    try:
        for result in results:
            property_ref.document(result['property_id']).set(result)
    except Exception as e:
        print(e)

    return results


def update_database():
    url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"

    querystring = {"city": "Atlanta",
                   "limit": "200",
                   "offset": "0",
                   "state_code": "GA",
                   "sort": "relevance"}

    headers = {
        'x-rapidapi-key': "YOUR-API-KEY",
        'x-rapidapi-host': "realtor.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    results = response.json()['properties']
    try:
        for result in results:
            property_ref.document(result['property_id']).set(result)
    except Exception as e:
        print(e)


# update the database with new data from API every week
sched = BackgroundScheduler(daemon=True)
sched.add_job(update_database, 'interval', weeks=1)
sched.start()