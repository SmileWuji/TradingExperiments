import numpy as np

def forward_fill(a):
    idx = np.where(np.isfinite(a), np.arange(a.shape[0]), 0)
    np.maximum.accumulate(idx, axis=0, out=idx)
    return a[idx]
