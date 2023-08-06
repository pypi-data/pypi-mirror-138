#!/usr/bin/env python


import gzip
import shutil
import os


def gzip_file(input, output, keep=False):
    with open(input, 'rb') as f_in:
        with gzip.open(output, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    if not keep:
        os.remove(input)


def sum_bgc_table(df):
    """The input dataframe with the index of id"""
    df['sum'] = df.sum(axis=1)
    sum_col = df.pop('sum')
    df.insert(0, 'sum', sum_col)
    return df