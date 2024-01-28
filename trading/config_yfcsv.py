import logging
import yfinance as yf

log = logging.getLogger('TradingExperiment')

REFERENCE_INDEX_TICKER_NAME = '^SPX'
REFERENCE_VOLATILITY_TICKER_NAME = '^VIX'
REFERENCE_RISK_FREE_TICKER_NAME = '^TNX'

# A simple parser of... one ticker_name per line
def parse_config(config):
    lst = list()
    with open(config, 'r') as fs:
        for line in fs:
            line = line.strip()
            if len(line) == 0:
                continue
            lst.append(line)
    return lst

def pull_data(out_dir, lst, suppress_exception=True):
    out_dir = out_dir.rstrip('/')
    a = yf.download(REFERENCE_INDEX_TICKER_NAME, periods="max", progress=False)
    a.to_csv(out_dir + '/_index.csv')

    a = yf.download(REFERENCE_VOLATILITY_TICKER_NAME, periods="max", progress=False)
    a.to_csv(out_dir + '/_volatility.csv')

    a = yf.download(REFERENCE_RISK_FREE_TICKER_NAME, periods="max", progress=False)
    a.to_csv(out_dir + '/_risk_free.csv')

    component_path = out_dir + '/{}_history.csv'
    for ticker_name in lst:
        try:
            pd = yf.download(ticker_name, progress=False)
            if pd is None or pd.shape[0] == 0:
                continue
            pd.to_csv(component_path.format(ticker_name))
        except Exception as e:
            if suppress_exception:
                log.error('{}: {}'.format(ticker_name, e))
            else:
                raise e
