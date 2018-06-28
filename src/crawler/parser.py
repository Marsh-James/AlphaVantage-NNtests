import json
import os
# Really basic parser I scrambled out his morning over breakfast. Far from perfect, just get's the job done right now
# Takes the json file from the crawler and formats the data to something more readable

def parse():

    with open(os.path.join('./reuterscrawler/reuterscrawler/spiders/out', "titles.json"), 'r') as f:
        # Each line in the titles.json file is a json object, so we just take each one and parse it independently
        for line in f:
            data = json.loads(line)
            title = data['title']
            symbol = data['symbol']
            date = data['date']

            # Strip out leading blanks and new line tags
            title = title.lstrip('\n')
            title = title.lstrip(' ')
            title = title.rstrip('| Reuters')

            # Symbols are always found infront of the equals sign in the html data
            symbol = symbol[symbol.find('=') + 1 : len(symbol)]

            # Split date and time into two entities, order of processing makes life easier by splitting things
            # Relative to '/', as seen in the example unparsed data below
            time = date[date.find('/') + 1: len(date)]
            time = time[0 : time.find('/')]
            time = time.lstrip(' ')
            time = time.rstrip(' ')

            date = date[0 : date.find('/') - 1]

            # Dumps into file, does not regenerate file so it must be removed before each startup
            if not os.path.exists("./parsed/"):
                os.makedirs("./parsed/")
            with open(os.path.join("./parsed/", "titles.json"), 'a') as out_file:
                dump = {'title': title, 'symbol': symbol, 'date': date, 'time': time}
                print(dump)
                out = json.dumps(dump)
                out_file.write(out+"\n")

parse()
    #{
    #    "title": "\n                Exclusive: U.S. may soon claim up to $1.7 billion penalty from China's ZTE  - sources | Reuters",
    #    "symbol": "/business/quotes/overview?symbol=000063.SZ", "date": "June 1, 2018 /  8:02 PM / a month ago"}