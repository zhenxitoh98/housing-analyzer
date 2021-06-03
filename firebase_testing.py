# for storing data into database
import requests
from firebase_admin import credentials, firestore, initialize_app
import pandas as pd

GA_DF = pd.read_csv('GA_City.csv')
GA_cities = GA_DF['name'].values.tolist()

AL_DF = pd.read_csv('AL_City.csv')
AL_cities = AL_DF['name'].values.tolist()

cred = credentials.Certificate("CONNECT-TO-FIREBASE")
default_app = initialize_app(cred)
db = firestore.client()
property_ref = db.collection('property')

url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"

# for city in GA_cities:
#     querystring = {"city": city,
#                    "limit": "30",
#                    "offset": "0",
#                    "state_code": "GA",
#                    "sort": "relevance"}
#
#     headers = {
#         'x-rapidapi-key': "CONNECT-TO-FIREBASE",
#         'x-rapidapi-host': "realtor.p.rapidapi.com"
#     }
#
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     results = response.json()['properties']
#     try:
#         for result in results:
#             property_ref.document(result['property_id']).set(result)
#     except Exception as e:
#         print(e)

for city in AL_cities:
    querystring = {"city": city,
                   "limit": "30",
                   "offset": "0",
                   "state_code": "AL",
                   "sort": "relevance"}

    headers = {
        'x-rapidapi-key': "CONNECT-TO-FIREBASE",
        'x-rapidapi-host': "realtor.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    results = response.json()['properties']
    try:
        for result in results:
            property_ref.document(result['property_id']).set(result)
    except Exception as e:
        print(e)