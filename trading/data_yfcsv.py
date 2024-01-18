import csv
import numpy as np
import os
import re

MARKET_DATA_FILE_RE = re.compile(r'(.*?)_history\.csv')

def market_data(market_data_path):
    reference_date, reference_trading_day = _reference_date(market_data_path)

    index = None
    with open(market_data_path + '/_index.csv', 'r') as fs:
        index = _yfcsv(reference_date, fs)

    risk_free = None
    with open(market_data_path + '/_risk_free.csv', 'r') as fs:
        risk_free = _yfcsv(reference_date, fs)

    volatility = None
    with open(market_data_path + '/_volatility.csv', 'r') as fs:
        volatility = _yfcsv(reference_date, fs)

    all_tickers = dict()
    for file_name in os.listdir(market_data_path):
        m = MARKET_DATA_FILE_RE.match(file_name)
        if m is None:
            continue
        ticker_name = m[1]
        with open(market_data_path + '/' + file_name) as fs:
            all_tickers[ticker_name] = _yfcsv(reference_date, fs)

    return {
        'reference_trading_day': reference_trading_day,
        'reference_date': reference_date,
        'index': index,
        'risk_free': risk_free,
        'volatility': volatility,
        'all_tickers': all_tickers,
    }

def _reference_date(market_data_path):
    reference_date = dict()
    reference_trading_day = list()

    with open(market_data_path + '/_index.csv') as fs:
        reader = csv.DictReader(fs)
        for row in reader:
            date = row['Date']
            trading_day = len(reference_trading_day)

            reference_trading_day.append(date)
            reference_date[date] = trading_day

    return reference_date, reference_trading_day

def _ticker(capacity):
    return {
        'adj_close': np.full(fill_value=np.nan, shape=(capacity,), dtype=np.float64),
        'volume': np.full(fill_value=np.nan, shape=(capacity,), dtype=np.float64),
    }

def _yfcsv(reference_date, fs):
    ticker = _ticker(len(reference_date))
    reader = csv.DictReader(fs)
    for row in reader:
        date = row['Date']
        if date not in reference_date:
            continue
        trading_day = reference_date[date]
        ticker['adj_close'][trading_day] = np.float64(row['Adj Close'])
        ticker['volume'][trading_day] = np.float64(row['Volume'])
    return ticker
