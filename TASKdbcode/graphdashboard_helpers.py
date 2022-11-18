
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
DEMOGRAPHIC_CATEGORY_DROPDOWN_LABELS = ["Race", "Language", "Age Range",\
                       "Gender", "Zip Code", "Homelessness", "Veteran Status",\
                       "Disability Status", "Guessed Status", "None"]

DEMOGRAPHIC_CATEGORY_DROPDOWN_VALUES = ["race", "language", "age_range",\
                       "gender", "zip_code", "homeless", "veteran",\
                       "disabled", "guessed", ""]


LANGUAGE_DROPDOWN_OPTIONS = [*database_constants.LANGUAGE_OPTIONS, "Any"]

AGE_RANGE_DROPDOWN_OPTIONS = [*database_constants.AGE_RANGE_OPTIONS, "Any"]

AGE_RANGE_DROPDOWN_OPTIONS = [*database_constants.AGE_RANGE_OPTIONS, "Any Age Range"]
AGE_RANGE_DROPDOWN_OPTIONS = [*database_constants.AGE_RANGE_OPTIONS, "Any Age Range"]
AGE_RANGE_DROPDOWN_OPTIONS = [*database_constants.AGE_RANGE_OPTIONS, "Any Age Range"]
AGE_RANGE_DROPDOWN_OPTIONS = [*database_constants.AGE_RANGE_OPTIONS, "Any Age Range"]


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
    
    for demographic_option, demographic_category in zip(database_constants.DEMOGRAPHIC_OPTIONS, database_constants.DEMOGRAPHIC_CATEGORIES):
        if demographic_option != selected_demographic:
            options_string = demographic_option.upper() + "_OPTIONS"
            # American Indian/Alaska Native
            # and Native Hawaiian/Pacific Islander
            # are too tall to fit in the default dropdown option height
            if demographic_option == "race":
                options_string = "RACE_DROPDOWN_OPTIONS"
                height = 80
            elif demographic_option == "zip_code":
                options_string = "ZIP_CODE_DROPDOWN_OPTIONS"
                height = 35
            else:
                height = 35
            if demographic_option in filter_dict.keys():
                filters.append(
                        dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                'name': demographic_option},
                                options=[{'value': o, 'label': o} for o in getattr(
                                    database_constants, options_string)],
                                clearable=True,
                                optionHeight=height,
                                multi=True,
                                value=filter_dict[demographic_option],
                                placeholder="Any " + demographic_category
                                ))
                    )
            else:
                filters.append(
                        dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                               'name': demographic_option},
                             options=[{'value': o, 'label': o} for o in getattr(
                                 database_constants, options_string)],
                             clearable=True,
                             multi=True,
                             value='',
                             optionHeight=height,
                             placeholder="Any " + demographic_category
                             ))
                    )
    return filters
#-----------------------------------------------------------------------

def construct_title(selected_demographic, filter_dict, graph_type):
    pass
    