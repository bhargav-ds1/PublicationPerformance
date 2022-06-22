from scholarly import ProxyGenerator
from scholarly import scholarly
import requests
pg = ProxyGenerator()
#pg.FreeProxies()

API_DOMAIN = 'https://ref.scholarcy.com'
POST_ENDPOINT = API_DOMAIN + '/api/references/extract'
params = {'reference_style': 'experimental', 'resolve_references': True, 'references': 'A. Egorov, A. König, M. Köppen, H. Kühn, I. Kullack, E. Kuthe, S. Mitkovska, R. Niehage, A. Pawelko, et al. Ressourcenbeschränkte Analyse von Ionenmobil- itätsspektren mit dem Raspberry Pi. Abschlussbericht der Projektgruppe 572 der Fakultät für Informatik. Technischer Bericht 5. TU Dortmund, May 2014 (cit. on p. 182).'}
r = requests.post(POST_ENDPOINT,
                              data=params,
                              # files=file_payload,
                              timeout=200
                )
r.encoding = 'utf-8'
bib = r.json()['bibtex']
