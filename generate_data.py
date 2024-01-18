from optparse import OptionParser
from optparse import OptionValueError

import os
import yfinance as yf

REFERENCE_INDEX_TICKER_NAME = '^SPX'
REFERENCE_VOLATILITY_TICKER_NAME = '^VIX'
REFERENCE_RISK_FREE_TICKER_NAME = '^TNX'

def parse_options():
    parser = OptionParser()
    parser.add_option("--out-dir", dest="out_dir", help="Directory name for data to persist")
    parser.add_option("--config", dest="config", help="File name a list of tickers to pull")
    (options, args) = parser.parse_args()
    if options.out_dir is None:
        raise OptionValueError("--out-dir is missing")
    if options.config is None:
        raise OptionValueError("--config is missing")
    return options

def parse_config(config):
    lst = list()
    with open(config, 'r') as fs:
        for line in fs:
            line = line.strip()
            if len(line) == 0:
                continue
            lst.append(line)
    return lst

if __name__ == '__main__':
    options = parse_options()
    lst = parse_config(options.config)

    out_dir = options.out_dir
    out_dir = out_dir.rstrip('/')
    os.mkdir(out_dir)

    a = yf.download(REFERENCE_INDEX_TICKER_NAME, periods="max")
    a.to_csv(out_dir + '/_index.csv')

    a = yf.download(REFERENCE_VOLATILITY_TICKER_NAME, periods="max")
    a.to_csv(out_dir + '/_volatility.csv')

    a = yf.download(REFERENCE_RISK_FREE_TICKER_NAME, periods="max")
    a.to_csv(out_dir + '/_risk_free.csv')

    component_path = out_dir + '/{}_history.csv'
    for ticker_name in lst:
        try:
            pd = yf.download(ticker_name)
            if pd is None or pd.shape[0] == 0:
                continue
            pd.to_csv(component_path.format(ticker_name))
        except Exception as e:
            print('{}: {}'.format(ticker_name, e))
    print('Done')
