import json
import os

def parse():

    with open(os.path.join('./reuterscrawler/reuterscrawler/spiders/out', "titles.json"), 'r') as f:
        for line in f:
            data = json.loads(line)
            title = data['title']
            symbol = data['symbol']
            date = data['date']

            title = title.lstrip('\n')
            title = title.lstrip(' ')
            title = title.rstrip('| Reuters')
            symbol = symbol[symbol.find('=') + 1 : len(symbol)]

            time = date[date.find('/') + 1: len(date)]
            time = time[0 : time.find('/')]
            time = time.lstrip(' ')
            time = time.rstrip(' ')

            date = date[0 : date.find('/') - 1]






            save_path = "./parsed/"
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            with open(os.path.join(save_path, "titles.json"), 'a') as out_file:
                dump = {'title': title, 'symbol': symbol, 'date': date, 'time': time}
                print(dump)
                out = json.dumps(dump)
                out_file.write(out+"\n")

parse()
    #{
    #    "title": "\n                Exclusive: U.S. may soon claim up to $1.7 billion penalty from China's ZTE  - sources | Reuters",
    #    "symbol": "/business/quotes/overview?symbol=000063.SZ", "date": "June 1, 2018 /  8:02 PM / a month ago"}