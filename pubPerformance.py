import sys
import os
import time
import logging
filePath = os.path.realpath(__file__)
dirPath = os.path.dirname(filePath)
sys.path.append(dirPath)
sys.path.append(dirPath+'/publikationstatistiken/pubStats')
from scopusApiTest import ScopusApiTest
from pubPerformanceDashboard import Dashboard


def getStats():
    st = ScopusApiTest('publikationstatistiken/pubStats/settings.yaml')
    df = st.scopus_get()
    db=Dashboard(df)
    db.app.run_server(debug = True)


if __name__ == '__main__':
    getStats()
