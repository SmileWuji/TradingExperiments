from .ptnd import ptnd_sma

import numpy as np

LATTICE_CACHE = dict()

def _internal_key(holding_period_days, aggregation_period_days, cache_key):
    return f'{holding_period_days}:{aggregation_period_days}:{cache_key}'

def _load_cache(holding_period_days, aggregation_period_days, cache_key):
    if cache_key is None:
        return None
    k = _internal_key(holding_period_days, aggregation_period_days, cache_key)
    if k not in LATTICE_CACHE:
        return None
    return LATTICE_CACHE[k]

def _write_cache(res, holding_period_days, aggregation_period_days, cache_key):
    if cache_key is None:
        return
    k = _internal_key(holding_period_days, aggregation_period_days, cache_key)
    LATTICE_CACHE[k] = res

def lattice_change_over_aggregaion_table(a, holding_period_days, aggregation_period_days,
        cache_key=None):
    res = _load_cache(holding_period_days, aggregation_period_days, cache_key)
    if res is not None:
        return res

    a_first_valid_idx = np.argwhere(np.isfinite(a))[0][0]
    a_sma = ptnd_sma(a, holding_period_days-1)

    # Average within the holding period
    num_periods = aggregation_period_days // holding_period_days
    a_agg_table = np.empty((num_periods, a_sma.shape[0],))
    for i in range(num_periods):
        a_agg_table[i, :] = np.roll(a_sma, i*holding_period_days)

    a_chg_table = a_agg_table / np.roll(a_agg_table, -1, axis=0)

    # Remove the last row as there is no "change"
    a_chg_table = a_chg_table[:-1, :]

    a_chg_table = a_chg_table - 1
    a_agg_table[:,:(a_first_valid_idx + aggregation_period_days)] = np.nan
    _write_cache(a_chg_table, holding_period_days, aggregation_period_days, cache_key)
    return a_chg_table

def lattice_historical_volatility(a, holding_period_days, aggregation_period_days, cache_key=None):
    a_chg_table = lattice_change_over_aggregaion_table(
        a, holding_period_days, aggregation_period_days, cache_key)
    result_std = np.std(a_chg_table, axis=0, ddof=1)
    result_std = result_std * np.power((252/holding_period_days), 0.5)
    return result_std

def lattice_historical_return(a, aggregation_period_days, cache_key=None):
    a_chg_table = lattice_change_over_aggregaion_table(
        a,
        aggregation_period_days,
        2*aggregation_period_days)
    return a_chg_table[0]

def lattice_positive_rate(a, holding_period_days, aggregation_period_days, cache_key=None):
    a_chg_table = lattice_change_over_aggregaion_table(
        a, holding_period_days, aggregation_period_days, cache_key)
    num_periods = aggregation_period_days // holding_period_days

    result = np.sum((a_chg_table > 0), axis=0) / num_periods
    return result

def lattice_correlation(lhs, rhs, holding_period_days, aggregation_period_days,
        lhs_cache_key=None, rhs_cache_key=None):
    lhs_ret_table = lattice_change_over_aggregaion_table(lhs, holding_period_days, aggregation_period_days,
        lhs_cache_key)
    rhs_ret_table = lattice_change_over_aggregaion_table(rhs, holding_period_days, aggregation_period_days,
        rhs_cache_key)

    lhs_chg_avg = np.mean(lhs_ret_table, axis=0)
    rhs_chg_avg = np.mean(rhs_ret_table, axis=0)

    lhs_basis = lhs_ret_table - lhs_chg_avg
    rhs_basis = rhs_ret_table - rhs_chg_avg

    mix_basis_ss = np.sum((lhs_basis * rhs_basis), axis=0)
    lhs_basis_ss = np.sqrt(np.sum((lhs_basis * lhs_basis), axis=0))
    rhs_basis_ss = np.sqrt(np.sum((rhs_basis * rhs_basis), axis=0))

    result = mix_basis_ss / (lhs_basis_ss * rhs_basis_ss)
    return result

def lattice_beta(a, index, holding_period_days, aggregation_period_days,
        a_cache_key=None, index_cache_key=None):
    a_ret_table = lattice_change_over_aggregaion_table(
        a, holding_period_days, aggregation_period_days, a_cache_key)
    index_ret_table = lattice_change_over_aggregaion_table(
        index, holding_period_days, aggregation_period_days, index_cache_key)

    a_chg_avg = np.mean(a_ret_table, axis=0)
    index_chg_avg = np.mean(index_ret_table, axis=0)

    a_basis = a_ret_table - a_chg_avg
    index_basis = index_ret_table - index_chg_avg

    mix_basis_ss = np.sum((a_basis * index_basis), axis=0)
    index_variance = np.sum((index_basis * index_basis), axis=0)
    return (mix_basis_ss / index_variance)
