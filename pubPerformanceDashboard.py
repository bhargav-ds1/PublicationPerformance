from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px

class Dashboard:
    def __init__(self,df):
        self.df = df
        BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
        self.app = Dash(__name__,external_stylesheets = [dbc.themes.CYBORG])
        self.app.layout = self.get_layout()
        self.app.callback(
        Output(component_id='bar-graph', component_property='figure'),
        Output(component_id='table-container',component_property='children'),
        Input(component_id='year_dropdown', component_property='value'),
        Input(component_id='select_dropdown', component_property='value'))(self.update_graph)


    # Set up the callback functiona
    def update_graph(self,selected_year,select_top):
        filtered_df = self.df
        if selected_year == 'all_values':
            text = str(filtered_df.year.min()) + "-" + str(filtered_df.year.max())
        else:
            filtered_df = filtered_df[filtered_df['year'] == selected_year]
            text = str(selected_year)

        if select_top == 't10':
            filtered_df = filtered_df.sort_values(['citedby-count'],ascending=False).head(10)
        elif select_top == 't50':
            filtered_df = filtered_df.sort_values(['citedby-count'],ascending=False).head(50)
        elif select_top == 't100':
            filtered_df = filtered_df.sort_values(['citedby-count'],ascending=False).head(100)
        elif select_top == 'b10':
            filtered_df = filtered_df.sort_values(['citedby-count'],ascending=True).head(10)
        elif select_top == 'b50':
            filtered_df = filtered_df.sort_values(['citedby-count'],ascending=True).head(50)
        elif select_top == 'b100':
            filtered_df = filtered_df.sort_values(['citedby-count'],ascending=True).head(100)
        elif select_top == 'All':
            filtered_df = filtered_df

        bar_fig = px.bar(filtered_df,x='dc:title',y='citedby-count',labels={'citedby-count':'Number of citations',
                                                               'dc:title':'Publications'})
        #bar_fig.update_traces(width = 2)
        bar_fig.update_layout(
                title={'text': f'Citation counts of {filtered_df.shape[0]} publications published in year {text}',
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                xaxis={'showticklabels':False},hovermode='x',bargap = 0.5)
        table = dbc.Table.from_dataframe(filtered_df[['dc:title','dc:creator',
                                                      'prism:coverDate','prism:doi',
                                                      'citedby-count']].rename(
            columns = {'dc:title':'Title','dc:creator':'First Author','prism:coverDate':'Date','prism:doi':'DOI',
                       'citedby-count':'citedby-count'}
        ), striped=True, bordered=True, hover=True)
        return bar_fig,table

    def get_layout(self):
        # Set up the app layout
        year_dropdown = dcc.Dropdown(id='year_dropdown',
                            options=[{'label': 'Select year (All)', 'value': 'all_values'}]+
                            [{'label':x, 'value':x} for x in sorted(self.df['year'].unique(),reverse=True)],
                            value='all_values')

        select_dropdown = dcc.Dropdown(id='select_dropdown',
                                       options=[{'label':'Select top/bottom percentage (All)','value':'All'},
                                                {'label':'Top 10','value':'t10'},
                                                {'label':'Top 50','value':'t50'},
                                                {'label':'Top 100','value':'t100'},
                                                {'label':'Bottom 10','value':'b10'},
                                                {'label':'Bottom 50','value':'b50'},
                                                {'label':'Bottom 100','value':'b100'}],
                                       value='All')


        return html.Div(children=[
            html.H1(children='Publication Performance based on number of citations.'),
            year_dropdown,
            select_dropdown,
            dcc.Graph(id='bar-graph'),
            html.Div(id='table-container')
        ])
# Run local server
if __name__ == '__main__':
    db=Dashboard()
    db.app.run_server(debug=True)
