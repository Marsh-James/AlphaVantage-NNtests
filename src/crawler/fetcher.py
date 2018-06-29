from alpha_vantage.timeseries import TimeSeries
import src.crawler.constants as c
from pprint import pprint
import os
import json

# Symbol filtering required before this
ts = TimeSeries(key=c.AV_KEY)
with open(os.path.join('./parsed', "titles.json"), 'r') as f:
    # Each line in the titles.json file is a json object, so we just take each one and parse it independently
    for line in f:
        data = json.loads(line)
        title = data['title']
        symbol = data['symbol']
        date = data['date']
        time = data['time']
        market_open_time = '10:00:00' # from data point's im getting, this is the shortest time I can get. Eastern time
        next_time_interval = '11:00:00'

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