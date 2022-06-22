from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

class Dashboard:
    def __init__(self,df):
        self.df = df
        self.app = Dash(__name__)
        self.app.layout = self.get_layout()
        self.app.callback(
        Output(component_id='price-graph', component_property='figure'),
        Input(component_id=geo_dropdown, component_property='value'))(update_graph)

    # Set up the callback function
    def update_graph(self,selected_geography):
        filtered_avocado = avocado[avocado['geography'] == selected_geography]
        line_fig = px.line(filtered_avocado,
                               x='date', y='average_price',
                               color='type',
                               title=f'Avocado Prices in {selected_geography}')
        return line_fig

    def get_layout(self):
        # Set up the app layout
        geo_dropdown = dcc.Dropdown(options=self.df['geography'].unique(),
                                    value='New York')

        return html.Div(children=[
            html.H1(children='Avocado Prices Dashboard'),
            geo_dropdown,
            dcc.Graph(id='price-graph')
        ])
# Run local server
if __name__ == '__main__':
    db=Dashboard()
    db.app.run_server(debug=True)
