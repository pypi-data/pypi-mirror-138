#!/usr/bin/env python


from psmpar import default
import pandas as pd

class BGCFeature():
    def __init__(self):
        self.database = self.read_bgc_database()


    def read_bgc_database(self, input=default.bgc_database):
        bgc_database= pd.read_csv(input, sep='\t', compression='gzip').set_index(['id'])
        bgc_database.fillna(0, inplace=True)
        return bgc_database

    def get_bgc_feature(self, query):
        target_bgc_feature = self.database.loc[query]
        return target_bgc_feature


