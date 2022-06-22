"""An example program that uses the elsapy module"""

import json
import os,sys
import re
from tqdm import tqdm
from collections import OrderedDict
import requests
import pandas as pd
import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text
from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch

filePath = os.path.realpath(__file__)
dirPath = os.path.dirname(filePath)
sys.path.append(dirPath + '/publikationstatistiken/pubStats')

from Handler import Handler
from BibHandler import BibHandler
from pdfHandler import pdfHandler


class ScopusApiTest(Handler):
    def __init__(self, settings_path):
        super().__init__(settings_path)
        self.settings_path = settings_path
        self.filenames = self.read_yaml()['pdfs']
        self.filenames = list(map(lambda a:a.split('.')[0]+".txt" if '.pdf' in a else a,self.filenames))
        ## Load configuration
        self.con_file = open("config.json")
        self.config = json.load(self.con_file)
        self.con_file.close()
        self.titles = []
    def get_titles_scholary_api(self,li,liNA):
        ref = '\n'.join(liNA)
        API_DOMAIN = 'https://ref.scholarcy.com'
        POST_ENDPOINT = API_DOMAIN + '/api/references/extract'
        params = {'reference_style': 'experimental', 'resolve_references': True, 'references': ref}
        r = requests.post(POST_ENDPOINT,
                                      data=params,
                                      # files=file_payload,
                                      timeout=200
                        )
        r.encoding = 'utf-8'
        bib = r.json()['bibtex']
        print(bib)
        file = bib.split('}\n')
        titles = list(map(lambda a:re.findall('\stitle\s=\s{.+},',a),file))
        print(titles)
        titles = [val for sublist in titles for val in sublist]
        titles = list(map(lambda a:a.split('title = {')[1].split('},')[0].split('.')[0],titles))
        print(titles)
        print(len(liNA))
        print(len(titles))
    def get_titles(self):
        # to get titles from the two Phase pdf's and the literature.bib file.
        #extract titles from the literature.bib file
        bibH = BibHandler(self.settings_path)
        bibH.download_literatur()
        with open(os.path.dirname(self.settings_path)+'/literatur.bib','r') as bibtexfile:
            file = bibtexfile.read()
            file = file.split('}\n')
            file = list(filter(lambda a: 'SFB' in a or 'sfb' in a,file))
            titles = list(map(lambda a:re.findall('\stitle\s=\s{.+},',a),file))
            titles = [val for sublist in titles for val in sublist]
            titles = list(map(lambda a:a.split('title = {')[1].split('},')[0],titles))
            titles = list(map(lambda a:LatexNodes2Text().latex_to_text(a),titles))
            titles = list(map(lambda a:re.sub(' +',' ',a),titles))
            self.titles.extend(titles)
            print(len(self.titles))
        # extract titles from reference text from pdf's using regex
        li = []
        liNA = []
        if not os.path.exists(any(self.filenames)):
            pdfH = pdfHandler(self.settings_path)
            pdfH.ref_from_pdfs_As_csv()
        for filename in self.filenames:
            if filename == 'Vollantrag_Phase3.txt':
                with open(filename,'r',encoding='utf-8') as f:
                    for line in f:
                        ref = line.strip()
                        if '“' in ref:
                            title = ref.split('“')[1]
                            title = title.split('”')[0]
                            li.append(title)
                        else:
                            li.append('NA')
                            liNA.append(ref)
            if filename == 'Vollantrag_Phase2.txt':
                with open(filename,'r',encoding='utf-8') as f:
                    for line in f:
                        ref = line.strip()
                        if '„' in ref:
                            title = ref.split('„')[1]
                            title = title.split('“')[0]
                            li.append(title)
                        else:
                            li.append('NA')
                            liNA.append(ref)
        #self.get_titles_scholary_api(li,liNA)
        self.titles.extend(li)
        #removing duplicate titles
        self.titles = list(OrderedDict.fromkeys(self.titles))
        print(len(self.titles))



    def scopus_get(self):
        self.get_titles()
        #print(*self.titles,sep='\n')
        ## Initialize scopus client
        self.client = ElsClient(self.config['apikey'])
        # client.inst_token = config['insttoken']
        # Get titles from the .txt file using regex
        df = pd.DataFrame()

        ## Initialize doc search object using Scopus and execute search, retrieving
        #   all results
        print('Running scopus query for '+str(len(self.titles))+' titles.')
        try:
            for i in tqdm(self.titles):
                doc_srch = ElsSearch(
                            "TITLE({"+i+"})",
                            'scopus')
                doc_srch.execute(self.client, get_all=True)
                #print("doc_srch has", len(doc_srch.results), "results.")
                #print(doc_srch.results)
                if len(doc_srch.results) ==1 and 'error' in doc_srch.results[0].keys():
                    out = pd.DataFrame([{'dc:title':i}])
                    df = pd.concat([df,out],ignore_index=True)
                else:
                    out = pd.DataFrame(doc_srch.results)
                    df = pd.concat([df,out],ignore_index=True)
            print(df)
            df.to_csv('scopus-results'+str(len(self.titles))+'.csv')
            return df
        except Exception as e:
            print(e)
            df.to_csv('scopus-results-partial'+str(len(self.titles))+'.csv')


if __name__ == '__main__':
    st = ScopusApiTest('publikationstatistiken/pubStats/settings.yaml')
    st.scopus_get()
