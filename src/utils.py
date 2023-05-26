import os
import sys
import pandas as pd
from glob import glob

# Launch via installed executable
import src.const as const

pynsist_prefix = 'pkgs/src'


# # launch in terminal
# import const as const
# pynsist_prefix = 'pkgs/src'


def get_file_names():
    return glob(f'{pynsist_prefix}/to_update/*')


def read_csv_as_df(file_name):
    if not os.path.isfile(file_name):
        return pd.DataFrame(columns=const.COLUMNS)
    else:
        import streamlit as st
        return pd.read_csv(file_name, encoding='utf-16')


def check_if_dir_exists(dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
