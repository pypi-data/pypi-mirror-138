import pandas as pd

def read_or_create_csv(filename, columns, index_col=[0]):
    try:
        df = pd.read_csv(filename, index_col=index_col)
    except FileNotFoundError:
        print(f"Pandas file {filename} not found...creating!")
        df = pd.DataFrame(columns = columns)
    except pd.errors.EmptyDataError:
        print(f"Pandas file {filename} not found...creating!")
        df = pd.DataFrame(columns = columns)
    return df

# def append(df, data, columns = None):
#     if isinstance(data, dict):
#         return pd.concat([df, pd.DataFrame(data)])
#     if isinstance(data, list) and columns is not None:
#         return pd.concat([df, pd.DataFrame(data)])