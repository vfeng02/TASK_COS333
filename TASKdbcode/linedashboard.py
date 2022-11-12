#!/usr/bin/env python

#-----------------------------------------------------------------------
# linedashboard.py
# Author: Andres Blanco Bonilla
# Dash app for line graph display
# route: /lineapp
#-----------------------------------------------------------------------

"""Instantiate a Dash app."""
import dash
import pandas
from TASKdbcode import demographic_db
from TASKdbcode import database_constants
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from TASKdbcode import graphdashboard_helpers as helpers

# this is my idea for the line graph menu, definitely not final

def init_liedashboard(server):
    line_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/lineapp/",
        external_stylesheets=[dbc.themes.BOOTSTRAP])

    df = demographic_db.get_patrons()
    demographic_options = []
    for option in database_constants.DEMOGRAPHIC_OPTIONS:
        demographic_options.append(
            {"label": option.replace("_", " ").title(), "value": option})

    line_app.layout = html.Div(
        children=[
            html.Div(children=[
                html.H4("Select a Date Range"),
                dcc.DatePickerRange(id='range',
                             options=demographic_options,
                             clearable=True,
                             value=''
                             ),
                html.H4(
                    "Select Meal Sites (Clear Selections to Select All Sites)"),
                dcc.Dropdown(id='site_options',
                             options=[{'value': o, 'label': o}
                                 for o in database_constants.MEAL_SITE_OPTIONS],
                             clearable=True,
                             multi=True,
                             value=["First Baptist Church"]
                             ),
                html.H4("Group Together or Separate Meal Sites?"),
                html.H5("If Group is selected, data for selected meal sites will be grouped together into one line on the graph"),
                html.H5("If Seperate is selected, each selected meal site will get its own line on the graph"),
                dcc.RadioItems(['Group', 'Separate'], 'Separate', inline=True),
                html.H4("Select Filters"),
                dbc.Row(id="filter_options", children=helpers.filter_options_helper(None, {})),

            ], className='menu-l'
            ),
            dcc.Graph(id='line_graph',
                      config={'displayModeBar': True,
                          'displaylogo': False},
                      className='card',
                      style={'width': '100vw', 'height': '100vh'}
                      )
        ]
    )

    init_callbacks(line_app)
    line_app.enable_dev_tools(
    dev_tools_ui=True,
    dev_tools_serve_dev_bundles=True,)

    return line_app.server

def init_callbacks(line_app):
    pass

