import numpy as np

def db_consolidate(db):
    '''
    Consolidates db into a table
    '''
    _, ref_a = next(iter(db.items()))
    table_index = list(db.keys())

    table = np.empty((len(table_index), ref_a.size), dtype=np.float64)
    for i in range(len(table_index)):
        table[i] = db[table_index[i]]

    return (table, table_index)

def db_rank(db):
    '''
    Assigns a rank to the time series in db.
    The order is sorted from small, to large, then to np.nan

    >>> my_db = {'ticker_a': np.array([1.1, 1.1, 1.1, 1.1, 0.8]),
    ...          'ticker_b': np.array([1.2, 1.2, 1.2, 1.2, 1.1]),
    ...          'ticker_c': np.array([1.0, 1.0, np.nan, 1.0, 1.0]}
    >>> my_db_rank = db_rank(my_db)
    >>> print(my_db_rank.keys())
    >>> print(my_db_rank['ticker_a'])
    >>> print(my_db_rank['ticker_b'])
    >>> print(my_db_rank['ticker_c'])

    # dict_keys(['ticker_a', 'ticker_b', 'ticker_c'])
    # array([1, 1, 0, 1, 0], dtype=int64)
    # array([2, 2, 1, 2, 2], dtype=int64)
    # array([0, 0, 2, 0, 1], dtype=int64)
    '''
    table, table_index = db_consolidate(db)

    order = np.argsort(table, axis=0)
    rank = np.argsort(order, axis=0)

    db_res = dict()
    for i in range(len(table_index)):
        ticker_name = table_index[i]
        a = rank[i]
        db_res[ticker_name] = a
    return db_res
