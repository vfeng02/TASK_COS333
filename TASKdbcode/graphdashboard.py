#!/usr/bin/env python

# -----------------------------------------------------------------------
# graphdashboard.py
# Author: Andres Blanco Bonilla
# Test
# -----------------------------------------------------------------------

"""Instantiate a Dash app."""
import dash
from TASKdbcode import demographic_db
from TASKdbcode import database_constants
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.graph_objects as go


def init_graphdashboard(server):
    graph_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/graphapp/")
    
    df = demographic_db.get_patrons([], {})
    demographic_options = []
    for option in database_constants.DEMOGRAPHIC_OPTIONS:
        demographic_options.append({"label": option.title(), "value": option})

    graph_app.layout = html.Div(
        children=[
            html.Div(children=[
                dcc.Dropdown(id='dropdown1',
                             options=[{'value': x, 'label': x}
                                      for x in df.meal_site.unique()],
                             clearable=False,
                             value='First Baptist Church',
                             ),
                dcc.Dropdown(id='dropdown2',
                             options=demographic_options,
                             clearable=False,
                             value='race',
                             )
            ], className='menu-l'
            ),
            dcc.Graph(id='interaction2',
                      config={'displayModeBar': False},
                      className='card')
        ]
    )
    
    init_callbacks(graph_app)

    return graph_app.server

def init_callbacks(graph_app):
    
    @graph_app.callback(
            Output('interaction2', 'figure'),
            [Input('dropdown1', 'value'),
                Input('dropdown2', 'value')]
        # B) defining the callback and what to return here
    )
    def update_pie_chart(select_d1,select_d2):
        df3 = demographic_db.get_patrons([], {"meal_site": select_d1})
        ## using dash to make the pie chart
        fig1=go.Figure(data=[go.Pie(labels=df3[select_d2].value_counts().index.tolist(),
                            values=list(df3[select_d2].value_counts()))])
        ## customizing the title of the pie chart
        fig1.update_layout(title=
            f"{select_d2.title()} of Patrons at {select_d1}"
                        " Meal Site")
        return fig1

