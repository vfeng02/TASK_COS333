
#!/usr/bin/env python

# -----------------------------------------------------------------------
# graphdashboard_helpers.py
# Author: Andres Blanco Bonilla
# Helper functions for graphing related dash apps, to reduce repeated
# code.
# -----------------------------------------------------------------------

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
import textwrap
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
def selected_fields_helper(callback_context):

    for key in list(callback_context.keys()):
        if "name" not in key:
            del callback_context[key]

    selected_fields = [eval(field.strip(".value"))
                       for field in list(callback_context)]
    selected_fields = [field["name"] for field in selected_fields]

    return selected_fields

# -----------------------------------------------------------------------


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
# -----------------------------------------------------------------------

def construct_title(filter_dict, graph_type, selected_demographic=None):
    
    filter_dict = {key:value for (key, value) in\
                   filter_dict.items() if value}
    
    category_dict = database_constants.DEMOGRAPHIC_CATEGORIES
    title = ""
    meal_sites = filter_dict.get("meal_site")
    if meal_sites:
        del filter_dict["meal_site"]

    if graph_type == "pie":
        title += "Percentage "
        if selected_demographic:
            title += f"distribution of <b>{category_dict[selected_demographic]}</b> among Diners "
        else:
            title += "of Diners "

        if filter_dict:
            title += "who are "
            filter_string = construct_filter_string(filter_dict)
            title += filter_string

        title = "<br>".join(textwrap.wrap(title, width= 100))

        if meal_sites:
            title+="<br>At "
            site_string = construct_site_string(meal_sites)
            title+=site_string
        else:
            title+="<br>Across all Meal Sites"

    if graph_type == "bar":
        
        if filter_dict:
            filter_string = construct_filter_string(filter_dict)
            title += filter_string
        
        title+="Diner Entries "
        
        if selected_demographic:
            title += f"by {category_dict[selected_demographic]} and "

        title+="by Meal Site"

    return title

# -----------------------------------------------------------------------


def construct_filter_string(filter_dict):
    status_options = database_constants.STATUS_OPTION_MAPPING
    
    filter_dict = {key:value for (key, value) in\
                   filter_dict.items() if value}

    if filter_dict.get("meal_site"):
        del filter_dict["meal_site"]

    filter_text_list = []
    filter_text_dict = {key:[] for (key, value) in filter_dict.items()}
    
    for key, value_list in filter_dict.items():
        for value in value_list:
            if key == "language":
                filter_text_dict[key].append(f"{value.title()}-speaking")
            elif key == "age_range":
                filter_text_dict[key].append(f"{value} years old")
            elif key == "zip_code":
                filter_text_dict[key].append(f"living at Zip Code {value}")
            elif key in list(status_options.keys()):
                filter_text_dict[key].append(status_options[key][value])
            else:
                filter_text_dict[key].append(value.title())
        if len(filter_text_dict[key]) > 1:
            filter_text = ' or '.join(
            filter_text_dict[key])
        else:
            filter_text = filter_text_dict[key][0]
        filter_text_list.append(filter_text)
        
    if len(filter_text_list) > 1:
        filter_string = ', '.join(
            filter_text_list[:-1]) + ', and ' + filter_text_list[-1] + " "
    else:
        filter_string = filter_text_list[0] + " "

    return filter_string
# -----------------------------------------------------------------------


def construct_site_string(meal_sites):
    site_string = ""
    if len(meal_sites) > 1:
        site_string = site_string+ \
            ', '.join(meal_sites[:-1]) + \
            ' and ' + meal_sites[-1]
    else:
        site_string+=meal_sites[0]

    return site_string
