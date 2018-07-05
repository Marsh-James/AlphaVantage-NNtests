import json
import os
import datetime

# Really basic parser I scrambled out his morning over breakfast. Far from perfect, just get's the job done right now
# Takes the json file from the crawler and formats the data to something more readable

def format_parsed():
    with open(os.path.join("./parsed/", "filtered_titles.json"), 'w') as init:
        init.write(json.dumps({}))

    with open(os.path.join('./parsed/', "titles.json"), 'r') as f:
        # Each line in the titles.json file is a json object, so we just take each one and parse it independently
        for line in f:
            data = json.loads(line)
            title = data['title']
            symbol = data['symbol']
            date = data['date']
            time = data['time']

            '''
            Filter criteria:
                            1) Not a weekend
                            2) times between 12:00:00 and 08:00:00
            '''

            # Dumps into file, does not regenerate file so it must be removed before each startup
            if not os.path.exists("./parsed/"):
                os.makedirs("./parsed/")
            with open(os.path.join("./parsed/", "filtered_titles.json"), 'r+') as output:
                new_obj = json.loads(output.read())
                new_obj[title] = {
                    "symbol": symbol,
                    "date": date,
                    "time": time
                }
                print(new_obj)
                output.seek(0)
                json.dump(new_obj, output)

format_parsed()
    #{
    #    "title": "\n                Exclusive: U.S. may soon claim up to $1.7 billion penalty from China's ZTE  - sources | Reuters",
    #    "symbol": "/business/quotes/overview?symbol=000063.SZ", "date": "June 1, 2018 /  8:02 PM / a month ago"}