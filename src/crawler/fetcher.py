from googlefinance.client import get_price_data
import firebase_admin
from firebase_admin import credentials, db
import json
import os

cred = credentials.Certificate('firebase_key.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://newsnet-cdf13.firebaseio.com'
})

def fetch():
    with open(os.path.join("./parsed/", "training_data.json"), 'w') as init:
        init.write(json.dumps({}))

    data = json.load(open('./parsed/filtered_titles.json'))

    for majorkey, subdict in data.items():

        title = majorkey
        symbol = subdict['symbol']
        date = subdict['date']

        params = {
            'q': symbol,  # Symbol
            'i': "3600",  # Interval (seconds)
            'x': 'LON',  # Exchange
            'p': "1Y"  # Period from today (d, Y)
        }

        try:

            historical_data = get_price_data(params)  # Updated local wrapper version to also return index as datetime
            json_port = json.loads(historical_data.to_json(orient='index'))

            market_open_time = '09:00:00'  # From data point's im getting, this is the shortest time I can get. UTC
            next_time_interval = '10:00:00'  # Assuming adding 1hr tracking time

            # Time key to verify day open existence
            time_key = str(date) + ' ' + str(market_open_time)
            if time_key in json_port:

                if int(json_port[date + ' ' + next_time_interval]['Close']) > int(json_port[date + ' ' + market_open_time]['Open']) * 1.03:
                    result = 1
                else:
                    result = 0
                if not os.path.exists("./final/") and result is not None:
                    os.makedirs("./final/")
                with open(os.path.join("./parsed/", "training_data.json"), 'r+') as output:
                    new_obj = json.loads(output.read())
                    new_obj[title] = result
                    output.seek(0)
                    print(new_obj)
                    json.dump(new_obj, output)
                db.reference('/').update({
                    title: result
                })
        except:
            print('Oops, something went wrong!')


fetch()
