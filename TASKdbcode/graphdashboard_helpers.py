
#!/usr/bin/env python

#-----------------------------------------------------------------------
# graphdashboard_helpers.py
# Author: Andres Blanco Bonilla
# Helper functions for graphing related dash apps, to reduce repeated
# code.
#-----------------------------------------------------------------------

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

#-----------------------------------------------------------------------
def selected_fields_helper(callback_context):
    
    for key in list(callback_context.keys()):
        if "name" not in key:
            del callback_context[key]

    selected_fields = [eval(field.strip(".value"))
                                for field in list(callback_context)]
    selected_fields = [field["name"] for field in selected_fields]
    return selected_fields

#-----------------------------------------------------------------------
def filter_options_helper(selected_demographic, filter_dict):
    
    filters = []
    
    for demographic_option in database_constants.DEMOGRAPHIC_OPTIONS:
        if demographic_option != selected_demographic:
            options_string = demographic_option.upper() + "_OPTIONS"
            if demographic_option in filter_dict.keys():
                filters.append(
                        dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                'name': demographic_option},
                                options=[{'value': o, 'label': o} for o in getattr(
                                    database_constants, options_string)],
                                clearable=True,
                                value=filter_dict[demographic_option],
                                placeholder=demographic_option.replace(
                                    "_", " ").title() + "..."
                                ))
                    )
            else:
                filters.append(
                        dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                               'name': demographic_option},
                             options=[{'value': o, 'label': o} for o in getattr(
                                 database_constants, options_string)],
                             clearable=True,
                             value='',
                             placeholder=demographic_option.replace(
                                 "_", " ").title() + "..."
                             ))
                    )
    return filters
#-----------------------------------------------------------------------
