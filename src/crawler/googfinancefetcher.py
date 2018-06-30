from googlefinance.client import get_price_data
import pandas as pd
import os
import json

params = {
    'q': "UKX",  # Symbol
    'i': "3600",  # Interval (seconds)
    'x': "INDEXFTSE",  # Exchange
    'p': "2d"  # Period from today (d, Y)
}

historical_data = get_price_data(params)
print(historical_data.to_json(orient='records')) # Starts furthest back works towards present
print(historical_data)
'''
with open(os.path.join('./parsed', "titles.json"), 'r') as f:
    # Each line in the titles.json file is a json object, so we just take each one and parse it independently
    for line in f:
        data = json.loads(line)
        title = data['title']
        symbol = data['symbol']
        date = data['date']
        time = data['time']
        market_open_time = '10:00:00' # From data point's im getting, this is the shortest time I can get. Eastern time
        next_time_interval = '11:00:00' # Assuming adding 1hr tracking time

        historical_data, meta_data = ts.get_intraday(symbol=symbol, interval='60min', outputsize='full')
        # Dates & times do not match format but it's just a rejig
        if historical_data[date + ' ' + market_open_time] is not None:
            result = None

            if historical_data[date + ' ' + next_time_interval]['4. close'] > \
                    historical_data[date + ' ' + market_open_time]['4. close']:
                result = 1
            else:
                result = 0
            if not os.path.exists("./final/"):
                os.makedirs("./final/")
            with open(os.path.join("./final/", "training_data.json"), 'a') as out_file:
                dump = {'title': title, 'symbol': symbol, 'date': date, 'time': time, 'result': result}
                print(dump)
                out = json.dumps(dump)
                out_file.write(out+"\n")
'''