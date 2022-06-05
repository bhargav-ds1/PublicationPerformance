import fitz
import re
from langdetect import detect, DetectorFactory
import requests
import bibtexparser
import pandas as pd
import os
timeout = 200

def ref_from_txt2bib2csv(filename):
    # using the post request-api provided by scholarcy which takes in references in text format and returns them as .bib
    # Storing the .bib returned by the post method of api to filename.bib file and converting this .bib to filename.csv
    # The api provides free access for extracting the references and will require an authentication by registering to
    # use the api for commercial purposes and for processing large files.

    #AUTH_TOKEN = 'abcdefg' # Your API key
    API_DOMAIN = 'https://ref.scholarcy.com'
    POST_ENDPOINT = API_DOMAIN + '/api/references/extract'
    #headers = {'Authorization': 'Bearer ' + AUTH_TOKEN}
    header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "text/plain"}
    file_path = './'+filename.split('.')[0]+'.txt'
    with open(file_path,'rb') as f:
        ref = f.read()
        if len(ref)<3: print("The plain text file consisting of bibliography extracted from pdf is empty.");return
        #print(ref)
        #file_payload = {'references':ref}
        params = {'reference_style': 'experimental', 'resolve_references': True,'references':ref}
        r = requests.post(POST_ENDPOINT,
            data=params,
            #files=file_payload,
            timeout=timeout)
        r.encoding = 'utf-8'
        bib = r.json()['bibtex']
        #print(bib)
    if len(bib)>5:
        with open(filename.split('.')[0]+'.bib','w',encoding='utf-8') as b:
            b.write(bib)

    with open(filename.split('.')[0]+'.bib','r',encoding='utf-8') as bibtexfile:
        bib_database = bibtexparser.load(bibtexfile)

    df = pd.DataFrame(bib_database.entries)
    df.rename(columns={'id': 'idCode'}, inplace=True)
    df.iloc[:,15] = df.iloc[:,15].astype(str).where(pd.notnull(df.iloc[:,15]), None)
    df.fillna('', inplace=True)
    df.to_csv('./'+filename.split('.')[0]+'.csv')
    os.remove(filename.split('.')[0]+'.bib')
    os.remove(filename.split('.')[0]+'.txt')


def ref_from_pdf2txt_EN(filename):
    with fitz.open(filename) as doc:
        #print(doc.page_count)
        text = ''
        flag = 0
        cnt=-1
        for page in doc:
            cnt+=1
            if flag == 1:
                flag = 0
                text += page.get_text()
            elif len(page.search_for("a) Peer-reviewed publications and books")) != 0:
                flag = 1
                text += page.get_text()
        #print(text)
        te= re.split('\[[a-zA-Z]+\w*/\w*/*\w*/*\d+]\s',text)
        #print(te)
        te = list(map(lambda a:a.replace('\n',' '),te))
        te = list(map(lambda a: a.split('3.4 Project plan')[0] if '3.4 Project plan' in a else a, te))
        te = list(filter(lambda a: 'a) Peer-reviewed publications and books' not in a, te))
        te = list(map(lambda a: a.split(' b) Other publications')[0] if 'b) Other publications' in a else a, te))
        te = list(map(lambda a: re.split('\s\d{2,3}\sProject',a)[0] if re.search('\d{2,3}\sProject',a) else a, te))
        te = list(map(lambda a: re.split('\s\[\d{2,3}]\s',a)[0] if re.search('\s\[\d{2,3}]\s',a) else a,te))
        #print(len(te))
        #print(te[0])
        if len(te)>5:
            with open(filename.split('.')[0]+'.txt','w',encoding='utf-8') as f:
                for item in te:
                    f.write("%s\n"%item)
                print("Completed extracting references from pdf to text file\nConverting the text file to .bib and "
                  "extracting the references from bib to CSV.")
        else: print("The references could not be extracted from pdf file.")

def ref_from_pdf2txt_DE(filename):
    with fitz.open(filename) as doc:
        #print(doc.page_count)
        text = ''
        flag = 0
        cnt=-1
        for page in doc:
            cnt+=1
            if flag == 1:
                flag = 0
                text += page.get_text()
            elif len(page.search_for("Begutachtete Publikationen")) != 0:
                flag = 1
                text += page.get_text()
        #print(text)
        te= re.split('\[[a-zA-Z]+\w*/\w*/*\w*/*\d+]\s',text)
        #print(te)
        te = list(map(lambda a:a.replace('\n',' '),te))
        te = list(map(lambda a: a.split('3.4 Planung des Teilprojekts')[0] if '3.4 Planung des Teilprojekts' in a else a, te))
        te = list(filter(lambda a: 'Begutachtete Publikationen' not in a, te))
        te = list(map(lambda a: a.split('Andere Veröffentlichungen')[0] if 'Andere Veröffentlichungen' in a else a, te))
        te = list(map(lambda a: re.split('\s\d{2,3}\s\w+\d+\s',a)[0] if re.search('\s\d{2,3}\s\w+\d+\s',a) else a, te))
        te = list(map(lambda a: re.split('\s\[\d{2,3}]\s',a)[0] if re.search('\s\[\d{2,3}]\s',a) else a,te))
        #print(len(te))
        #print(te[0])
        if len(te)>5:
            with open(filename.split('.')[0]+'.txt','w',encoding='utf-8') as f:
                for item in te:
                    f.write("%s\n"%item)
                print("Completed extracting references from pdf to text file\nConverting the text file to .bib and "
                  "extracting the references from bib to CSV.")
        else: print("The references could not be extracted from pdf file.")


if __name__ == '__main__':
    filename = 'Vollantrag_Phase3.pdf'
    with fitz.open(filename) as doc:
        #print(doc.get_toc()[0][1])
        DetectorFactory.seed = 0
        if detect(doc.get_toc()[0][1]) == 'en':
            ref_from_pdf2txt_EN(filename)
        if detect(doc.get_toc()[0][1]) == 'de':
            ref_from_pdf2txt_DE(filename)
        ref_from_txt2bib2csv(filename)




