import os

import pandas as pd
from glob import glob

# import src.const as const
import const as const


def get_file_names():
    return glob('src/to_update/*')


def read_csv_as_df(file_name):
    if not os.path.isfile(file_name):
        return pd.DataFrame(columns=const.COLUMNS)
    else:
        return pd.read_csv(file_name, encoding='utf-16')
