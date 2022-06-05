import requests
import bibtexparser
import pandas as pd
timeout = 200

#AUTH_TOKEN = 'abcdefg' # Your API key
API_DOMAIN = 'https://ref.scholarcy.com'
POST_ENDPOINT = API_DOMAIN + '/api/references/extract'
#headers = {'Authorization': 'Bearer ' + AUTH_TOKEN}
header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "text/plain"}
file_path = './reference_file.txt'
with open(file_path,'rb') as f:
    ref = f.read()
    #print(ref)
    #file_payload = {'references':ref}
    params = {'reference_style': 'ensemble', 'resolve_references': True,'references':ref}
    r = requests.post(POST_ENDPOINT,
        data=params,
        #files=file_payload,
        timeout=timeout)
    r.encoding = 'utf-8'
    bib = r.json()['bibtex']
    print(bib)
with open('Vollantrag_Phase3.bib','w',encoding='utf-8') as b:
    b.write(bib)

with open('Vollantrag_Phase3.bib','r',encoding='utf-8') as bibtexfile:
    bib_database = bibtexparser.load(bibtexfile)

df = pd.DataFrame(bib_database.entries)
df.rename(columns={'id': 'idCode'}, inplace=True)
df.iloc[:,15] = df.iloc[:,15].astype(str).where(pd.notnull(df.iloc[:,15]), None)
df.fillna('', inplace=True)
df.to_csv('./Vollantrag_Phase3.csv')
