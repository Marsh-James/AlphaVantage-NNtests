from iexfinance import get_historical_data
from datetime import datetime

start = datetime(2014, 2, 9)
end = datetime(2017, 5, 24)

df = get_historical_data("AAPL", start=start, end=end, output_format='pandas')
print(df)