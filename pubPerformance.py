import sys
import os
import time
import logging
filePath = os.path.realpath(__file__)
dirPath = os.path.dirname(filePath)
sys.path.append(dirPath)
sys.path.append(dirPath+'/publikationstatistiken/pubStats')

from Analyzer import Analyzer
from BibHandler import BibHandler
import pdfExtractor as pdfextract


def getStats():
    bibH = BibHandler(dirPath + "/publikationstatistiken/pubStats/" + "settings.yaml")
    analyzer = Analyzer()

    bibDF = bibH.getBib()
    pdfDF = pdfextract.ref_from_pdfs_As_csv()

    start = time.time()
    # analyzer.analyse_query(bibDF, coreDF)
    # analyzer.analyse_fuzzy(bibDF, coreDF)
    analyzer.analyse_sbert_cos(bibDF, pdfDF)
    finish = time.time()
    print(f'\n|-> Process finished sucessfully in {finish-start} s')
    print(f'|-> You may now take a look at the following link : \n\
            {analyzer.get_link()}')
    # logging.info(f'\n|-> Process finished sucessfully in {finish-start} s')
    # logging.info(f'|-> You may now take a look at the following link : \n\
    #         {analyzer.get_link()}')


if __name__ == '__main__':
    getStats()
