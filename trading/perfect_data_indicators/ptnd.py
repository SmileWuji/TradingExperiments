import numpy as np

def ptnd(a, n_days):
    '''
    Input: a      List[ts]
           n_days Number of days to look back

    Returns a 2D array List[ts: n_day] where List[ts, 0] = a and List[ts, 1] = ptnd_n_days(a)
    '''
    res = np.zeros(shape=(a.size, 2))
    res[:, 0] = a
    sh = np.roll(a, n_days)
    sh[:n_days] = np.nan
    res[:, 1] = sh

    offset = np.argmax(np.isfinite(sh))
    res[0:offset, 0] = np.nan
    res[0:offset, 1] = np.nan

    return res

def ptnd_table(a, n_days):
    '''
    Generalization of ptnd(a, n_days)
    '''
    res = np.zeros(shape=(a.size, n_days+1))
    for i in range(n_days+1):
        res[:, i] = np.roll(a, i)

    res[0:n_days, n_days] = np.nan
    offset = np.argmax(np.isfinite(res[:, n_days]))
    res[0:offset, :] = np.nan

    return res

def ptnd_sma(a, n_days):
    '''
    Returns the simple moving average of a using past n_days of data
    '''
    return np.average(ptnd_table(a, n_days), axis=1)

def ptnd_change_trendline(a, n_days):
    '''
    Returns the slopes m (of mx+b lines) with (closed form) linear regression
    (m is commonly denoted as β)
    '''
    # Build table
    y = ptnd_table(a, n_days)

    # Convert value to a change
    y = (y.T / y[:, -1]).T - 1

    # First day first row, last day last row
    y = np.flip(y, axis=1)

    x = np.arange(n_days+1, dtype=np.double)
    x_aug = np.array([x, np.ones(x.shape[0])]).T

    # Linear regression on each line
    factor = np.linalg.inv(np.matmul(x_aug.T, x_aug))
    partial_result = np.einsum('ij,ki->kj', x_aug, y)
    beta = np.einsum('ij,ki->kj', factor, partial_result)

    # Compute the loss of each line (MSE will be used)
    y_tilt = np.einsum('ij,kj->ki', x_aug, beta)
    diff = y_tilt - y
    loss = np.average(np.power(diff, 2), axis=1)

    return beta, loss

def ptnd_drawdown(a, n_days):
    table = ptnd_table(a, n_days)
    table = np.flip(table, axis=1)
    acc_table = np.maximum.accumulate(table, axis=1)
    drawdown_amt = (acc_table - table)
    drawdown_pct = drawdown_amt / acc_table
    return -np.max(drawdown_pct, axis=1)

def ptnd_percentile(a, q, n_days):
    '''
    Returns the q'th percentile using past n_days of data
    '''
    a_ptnd_table = ptnd_table(a, n_days)
    return np.percentile(a, q, axis=1)
