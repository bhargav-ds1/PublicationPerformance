import json
import os,sys

import pandas as pd
from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
con_file = open("config.json")
config = json.load(con_file)
con_file.close()
client = ElsClient(config['apikey'])

doc_srch = ElsSearch("TITLE({Measurement of the time-dependent \$CP\$ asymmetry in \$B\^0 \to J/\psi K\^0\_{\rm S}\$ decays})",'scopus')
doc_srch.execute(client, get_all=True)
print("doc_srch has", len(doc_srch.results), "results.")
print(doc_srch.results)
#df.append(doc_srch.results)
