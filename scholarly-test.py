'''from scholarly import ProxyGenerator
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
bib = r.json()['bibtex']'''

# Import libraries
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px

# Load the dataset
avocado = pd.read_csv('filtered.csv')

# Create the Dash app
app = Dash()

# Set up the app layout
geo_dropdown = dcc.Dropdown(id='year_dropdown',
                            options=[{'label':x, 'value':x} for x in avocado['year'].unique()] + [{'label': 'Select year', 'value': 'all_values'}],
                            value='all_values')

app.layout = html.Div(children=[
    html.H1(children='Avocado Prices Dashboard'),
    geo_dropdown,
    dcc.Graph(id='price-graph')
])


# Set up the callback function
@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id='year_dropdown', component_property='value')
)
def update_graph(selected_geography):
    if selected_geography == 'all_values':
        filtered_avocado = avocado
    else:
        filtered_avocado = avocado[avocado['year'] == selected_geography]
    line_fig = px.line(filtered_avocado,
                       x='year', y='citedby-count',
                       color='openaccess',
                       title=f'Avocado Prices in {selected_geography}')
    return line_fig


# Run local server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

