# Python module for downloading time series data
This repository gets data from the Alpha Vantage API: https://www.alphavantage.co/.
You need an API key in order to use the utilities in this repo. 

You can retrieve price data from many stocks traded in stock markets.

## Load Data
To use this module, you will need to have your own
Alpha Vantage API key.
```
from loaders import loader

data_loader = loader.TimeSeriesLoader(symbol="AAPL", interval=1)

df = data_loader.ts_intraday()

df_ext = data_loader.ts_intraday_extended(interval='5min&slice=year1month5')
```
