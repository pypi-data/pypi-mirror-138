from random import randint
from sklearn.model_selection import train_test_split

def tvp_split(df, sv, sp, seed=None):
    seed = seed if seed is not None else randint(1, 65535)
    sv, sp = sv + sp, sp/(sv + sp)
    dt, dv = train_test_split(df, test_size=sv, random_state=seed)
    dv, dp = train_test_split(dv, test_size=sp, random_state=seed)
    return dt, dv, dp