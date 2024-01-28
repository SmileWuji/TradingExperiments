from optparse import OptionParser
from optparse import OptionValueError

import trading.data_yfcsv as md
import trading.perfect_data_indicators as ind

import numpy as np
import os
import re

def parse_options():
    parser = OptionParser()
    parser.add_option("--in-dir", dest="in_dir", help="Directory for market data")
    (options, args) = parser.parse_args()
    if options.in_dir is None:
        raise OptionValueError("--in-dir is missing")
    return options

if __name__ == '__main__':
    options = parse_options()
    in_dir = options.in_dir
    in_dir = in_dir.rstrip('/')

    MARKET_DATA = md.market_data(in_dir)

    out_dir = in_dir + '-preprocessed'
    os.mkdir(out_dir)

    MARKET_DB = {
        ticker_name: ind.forward_fill(MARKET_DATA['all_tickers'][ticker_name]['adj_close'])
        for ticker_name in MARKET_DATA['all_tickers']
    }
    np.save(out_dir + '/MARKET_DB', MARKET_DB)

    np.save(out_dir + '/XS', MARKET_DATA['reference_trading_day'])
    np.save(out_dir + '/INDEX', MARKET_DATA['index']['adj_close'])
    np.save(out_dir + '/RISK_FREE', MARKET_DATA['risk_free']['adj_close'])
    np.save(out_dir + '/IV', MARKET_DATA['volatility']['adj_close'])

    HV_1_21_DB = dict()
    HV_5_63_DB = dict()
    HV_21_252_DB = dict()

    BETA_1_21_DB = dict()
    BETA_5_63_DB = dict()
    BETA_21_252_DB = dict()

    RETURN_21_DB = dict()
    RETURN_63_DB = dict()
    RETURN_252_DB = dict()

    for ticker_name in MARKET_DB:
        HV_1_21_DB[ticker_name] = ind.lattice_historical_volatility(MARKET_DB[ticker_name], 1, 21,
            cache_key=ticker_name)
        HV_5_63_DB[ticker_name] = ind.lattice_historical_volatility(MARKET_DB[ticker_name], 5, 63,
            cache_key=ticker_name)
        HV_21_252_DB[ticker_name] = ind.lattice_historical_volatility(MARKET_DB[ticker_name], 21, 252,
            cache_key=ticker_name)

        BETA_1_21_DB[ticker_name] = ind.lattice_beta(MARKET_DB[ticker_name], MARKET_DATA['index']['adj_close'], 1, 21,
            a_cache_key=ticker_name, index_cache_key='_index')
        BETA_5_63_DB[ticker_name] = ind.lattice_beta(MARKET_DB[ticker_name], MARKET_DATA['index']['adj_close'], 5, 63,
            a_cache_key=ticker_name, index_cache_key='_index')
        BETA_21_252_DB[ticker_name] = ind.lattice_beta(MARKET_DB[ticker_name], MARKET_DATA['index']['adj_close'], 21, 252,
            a_cache_key=ticker_name, index_cache_key='_index')

        RETURN_21_DB[ticker_name] = ind.lattice_historical_return(MARKET_DB[ticker_name], 21)
        RETURN_63_DB[ticker_name] = ind.lattice_historical_return(MARKET_DB[ticker_name], 63)
        RETURN_252_DB[ticker_name] = ind.lattice_historical_return(MARKET_DB[ticker_name], 252)

    np.save(out_dir + '/HV_1_21_DB', HV_1_21_DB)
    np.save(out_dir + '/HV_5_63_DB', HV_5_63_DB)
    np.save(out_dir + '/HV_21_252_DB', HV_21_252_DB)

    np.save(out_dir + '/BETA_1_21_DB', BETA_1_21_DB)
    np.save(out_dir + '/BETA_5_63_DB', BETA_5_63_DB)
    np.save(out_dir + '/BETA_21_252_DB', BETA_21_252_DB)

    np.save(out_dir + '/RETURN_21_DB', RETURN_21_DB)
    np.save(out_dir + '/RETURN_63_DB', RETURN_63_DB)
    np.save(out_dir + '/RETURN_252_DB', RETURN_252_DB)
