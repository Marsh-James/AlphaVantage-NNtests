from googlefinance.client import get_price_data
import pandas as pd
import os
import json

# LOOKS LIKE WE NEED TO FILTER WEEKEND STORIES AND ONLY KEEP WEEKDAYS!

params = {
    'q': "UKX",  # Symbol
    'i': "3600",  # Interval (seconds)
    'x': "INDEXFTSE",  # Exchange
    'p': "1Y"  # Period from today (d, Y)
}

historical_data = get_price_data(params) # Updated local wrapper version to also return index as datetime
json_port = historical_data.to_json(orient='index')

print(json_port) # Starts furthest back works towards present (9 records in a day)
# print(historical_data)

with open(os.path.join('./parsed', "titles.json"), 'r') as f:
    # Each line in the titles.json file is a json object, so we just take each one and parse it independently
    for line in f:
        data = json.loads(line)
        title = data['title']
        symbol = data['symbol']
        date = data['date']
        time = data['time']

        market_open_time = '08:00:00'  # From data point's im getting, this is the shortest time I can get. Eastern time
        next_time_interval = '09:00:00'  # Assuming adding 1hr tracking time

        # Dates & times do not match format but it's just a rejig
        if historical_data[date + ' ' + market_open_time] is not None:
            result = None

            if historical_data[date + ' ' + next_time_interval]['close'] > \
                    historical_data[date + ' ' + market_open_time]['close']:
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
