import json
import os
import datetime

# Really basic parser I scrambled out his morning over breakfast. Far from perfect, just get's the job done right now
# Takes the json file from the crawler and formats the data to something more readable

def format_parsed():
    with open(os.path.join("./parsed/", "filtered_titles.json"), 'w') as init:
        init.write(json.dumps({}))

    with open(os.path.join('./parsed/', "titles.json"), 'r') as f:
        count = 0
        # Each line in the titles.json file is a json object, so we just take each one and parse it independently
        for line in f:
            count += 1
            data = json.loads(line)
            title = data['title']
            symbol = data['symbol']
            date = data['date']
            time = data['time']

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
                print(count)
                output.seek(0)
                json.dump(new_obj, output)

format_parsed()