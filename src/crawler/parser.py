import json
import os
import datetime
import src.crawler.constants as c
# Really basic parser I scrambled out his morning over breakfast. Far from perfect, just get's the job done right now
# Takes the json file from the crawler and formats the data to something more readable

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']

def parse():

    with open(os.path.join('./reuterscrawler/reuterscrawler/spiders/out', "titles_january_18.json"), 'r') as f:
        # Each line in the titles.json file is a json object, so we just take each one and parse it independently
        for line in f:
            data = json.loads(line)
            title = data['title']
            symbol = data['symbol']
            date = data['date']
            try:
                # Strip out leading blanks and new line tags
                title = title.lstrip('\n')
                title = title.lstrip(' ')
                title = title.rstrip('| Reuters')

                # Symbols are always found infront of the equals sign in the html data
                symbol = symbol[symbol.find('=') + 1 : len(symbol)]

                # Split date and time into two entities, order of processing makes life easier by splitting things
                # Relative to '/', as seen in the example unparsed data below
                time = date[date.find('/') + 1: len(date)]
                time = time[0: time.find('/')]
                time = time.lstrip(' ')
                time = time.rstrip(' ')

                date = date[0: date.find('/') - 1]

                month = date[0:date.find(' ')]
                date = date[date.find(' ') + 1:len(date)]
                month = months.index(month) + 1
                if month < 10:
                    month = '0' + str(month)
                else:
                    month = str(month)

                day = date[0:date.find(',')]
                year = date[date.find(',') + 1:len(date)]

                if int(day) < 10:
                    day = '0' + str(day)

                formatted_date = year + '-' + month + '-' + day
                formatted_date = formatted_date.lstrip(' ')
                # print(date)
                # print(formatted_date)
                # print(year + '-' + month + '-' + day)
                # January 31, 2018 to 2018-01-31 08:00:00
                # time = data['time']s

                # print(date)
                # print((formatted_date[0:4]) + ' ' + (formatted_date[5:7]) + ' ' + (formatted_date[8:10]))
                dayNo = datetime.datetime(int(formatted_date[0:4]),
                                          int(formatted_date[5:7]),
                                          int(formatted_date[8:10]),
                                          hour=0, minute=0, second=0)

                # Weekned filter
                if dayNo.weekday() >= 0 and dayNo.weekday() < 5:
                    time_hour = time[0:time.find(':')]
                    time_ofDay = time[len(time) - 2:len(time)]
                    # print(time)
                    # print(time_hour)
                    # Filter for before market open
                    if 8 > int(time_hour) >= 0 and time_ofDay == 'AM':
                        formatted_symbol = symbol[0:symbol.find('.')]
                        if True:  # formatted_symbol in c.SYMBOLS:

                            # Dumps into file, does not regenerate file so it must be removed before each startup
                            if not os.path.exists("./parsed/"):
                                os.makedirs("./parsed/")
                            with open(os.path.join("./parsed/", "titles.json"), 'a') as out_file:
                                dump = {'title': title, 'symbol': formatted_symbol, 'date': formatted_date, 'time': time}
                                print(dump)
                                out = json.dumps(dump)
                                out_file.write(out+"\n")
            except:
                print("This broke")

parse()
    #{
    #    "title": "\n                Exclusive: U.S. may soon claim up to $1.7 billion penalty from China's ZTE  - sources | Reuters",
    #    "symbol": "/business/quotes/overview?symbol=000063.SZ", "date": "June 1, 2018 /  8:02 PM / a month ago"}