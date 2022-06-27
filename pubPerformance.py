import sys
import os

import pandas as pd

filePath = os.path.realpath(__file__)
dirPath = os.path.dirname(filePath)
sys.path.append(dirPath)
sys.path.append(dirPath+'/publikationstatistiken/pubStats')
from scopusApiTest import ScopusApiTest
from pubPerformanceDashboard import Dashboard


def getStats():
    st = ScopusApiTest('publikationstatistiken/pubStats/settings.yaml')
    df = st.scopus_get()
    df = clean_df(df)
    db=Dashboard(df)
    db.app.run_server(debug = True)

def clean_df(df):
    df.dropna(subset=['dc:identifier'],inplace=True)
    df = df.loc[df.astype(str).drop_duplicates().index]
    df['dc:identifier'] = df['dc:identifier'].str.strip("SCOPUS_ID:")
    df.set_index(['dc:identifier','dc:title'])
    df['year'] = pd.to_datetime(df['prism:coverDate']).dt.year
    df=df.astype({'openaccess':"category"})
    return df
if __name__ == '__main__':
    getStats()
