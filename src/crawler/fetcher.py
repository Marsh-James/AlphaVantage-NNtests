from googlefinance.client import get_price_data
import json
import os

data = json.load(open('./parsed/filtered_titles.json'))

for majorkey, subdict in data.items():

    title = majorkey
    symbol = subdict['symbol']
    date = subdict['date']
    time = subdict['time']

    params = {
        'q': symbol,  # Symbol
        'i': "3600",  # Interval (seconds)
        'x': 'LON',  # Exchange
        'p': "1Y"  # Period from today (d, Y)
    }

    try:

        historical_data = get_price_data(params)  # Updated local wrapper version to also return index as datetime
        json_port = json.loads(historical_data.to_json(orient='index'))

        market_open_time = '09:00:00'  # From data point's im getting, this is the shortest time I can get. Eastern time
        next_time_interval = '10:00:00'  # Assuming adding 1hr tracking time


        # Time key to verify day open existence
        time_key = str(date) + ' ' + str(market_open_time)
        print(time_key)
        if time_key in json_port:
            result = None

            if int(json_port[date + ' ' + next_time_interval]['Close']) > int(json_port[date + ' ' + market_open_time]['Open']) * 1.03:
                result = 1
                if not os.path.exists("./final/"):
                    os.makedirs("./final/")
                with open(os.path.join("./parsed/", "training_data.json"), 'a') as out_file:
                    dump = {'title': title, 'symbol': symbol, 'date': date, 'time': time, 'result': result}
                    print(dump)
                    out = json.dumps(dump)
                    out_file.write(out+"\n")
    except:
        print('break')
