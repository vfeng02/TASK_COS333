
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
import textwrap
import datetime
from flask_simplelogin import login_required

#-----------------------------------------------------------------------

def protect_dashviews(dashapp):
    """If you want your Dash app to require a login,
    call this function with the Dash app you want to protect"""

    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(
                dashapp.server.view_functions[view_func], must=[demographic_db.be_admin]
            )
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

# def table_buttons_helper():
#     button_option_list = []
#     for option in database_constants.DEMOGRAPHIC_OPTIONS:
#         button_option = {"label": f"{database_constants.DEMOGRAPHIC_CATEGORIES[option]} Counts", "value": option},
#         button_option_list.append(button_option)
#     button_option_list.append({"label": "All Counts", "value": "all"})
#     return button_option_list

#-----------------------------------------------------------------------

def selected_fields_helper(callback_context):
    # print(list(callback_context.keys()))

    for key in list(callback_context.keys()):
        if "name" not in key:
            del callback_context[key]

    selected_fields = [eval(field.strip(".value"))
                       for field in list(callback_context)]
    selected_fields = [field["name"] for field in selected_fields]
    print(selected_fields)

    return selected_fields

#-----------------------------------------------------------------------

def filter_options_helper(selected_demographic, filter_dict, graph_type):

    filters = []
    dem_row1 = []
    dem_row2 = []
    dem_row3 = []
    status_row1 = []
    status_row2 = []
    demographic_categories = database_constants.DEMOGRAPHIC_CATEGORIES

    for demographic_option in database_constants.DEMOGRAPHIC_OPTIONS:
        if demographic_option != selected_demographic:
            options_string = demographic_option.upper() + "_OPTIONS"
            # American Indian/Alaska Native
            # and Native Hawaiian/Pacific Islander
            # are too tall to fit in the default dropdown option height
            if demographic_option == "race":
                options_string = "RACE_DROPDOWN_OPTIONS"
            elif demographic_option == "zip_code":
                options_string = "ZIP_CODE_DROPDOWN_OPTIONS"
            
            height = 35

            if demographic_option in filter_dict.keys():
                if demographic_option in list(database_constants.STATUS_OPTION_MAPPING.keys()):
                    if demographic_option in ("homeless", "veteran"):
                        status_row1.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                                clearable=True,
                                                optionHeight=height,
                                                multi=True,
                                                value=filter_dict[demographic_option],
                                                placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    else:
                        status_row2.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                                clearable=True,
                                                optionHeight=height,
                                                multi=True,
                                                value=filter_dict[demographic_option],
                                                placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                else:
                    if demographic_option == "race":
                        dem_row1.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                                clearable=True,
                                                optionHeight=height,
                                                multi=True,
                                                value=filter_dict[demographic_option],
                                                placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    elif demographic_option in ("language", "age_range"):
                        dem_row2.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                                clearable=True,
                                                optionHeight=height,
                                                multi=True,
                                                value=filter_dict[demographic_option],
                                                placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    else:
                        dem_row3.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                                clearable=True,
                                                optionHeight=height,
                                                multi=True,
                                                value=filter_dict[demographic_option],
                                                placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    
                        
            else:
                if demographic_option in list(database_constants.STATUS_OPTION_MAPPING.keys()):
                    if demographic_option in ("homeless", "veteran"):
                        status_row1.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                    clearable=True,
                                    multi=True,
                                    value='',
                                    optionHeight=height,
                                    placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    else:
                        status_row2.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                    clearable=True,
                                    multi=True,
                                    value='',
                                    optionHeight=height,
                                    placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                else:
                    if demographic_option == "race":
                        dem_row1.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                    clearable=True,
                                    multi=True,
                                    value='',
                                    optionHeight=height,
                                    placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    elif demographic_option in ("language", "age_range"):
                        dem_row2.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                    clearable=True,
                                    multi=True,
                                    value='',
                                    optionHeight=height,
                                    placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    else:
                        dem_row3.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                    clearable=True,
                                    multi=True,
                                    value='',
                                    optionHeight=height,
                                    placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                
    dem_row1 = dbc.Row(dem_row1, className="gx-1", style = {"margin-bottom": "5px"})
    dem_row2 = dbc.Row(dem_row2, className="gx-1", style = {"margin-bottom": "5px"})
    dem_row3 = dbc.Row(dem_row3, className="gx-1", style = {"margin-bottom": "5px"})
    status_row1 = dbc.Row(status_row1, className="gx-1", style = {"margin-bottom": "5px"})
    status_row2 = dbc.Row(status_row2, className="gx-1", style = {"margin-bottom": "5px"})
    if dem_row1.children:
        filters = [dem_row1, dem_row2, dem_row3, status_row1, status_row2]   
    else:
        filters = [dem_row2, dem_row3, status_row1, status_row2]
    if graph_type != "line":
        start_date = None
        end_date = None
        if filter_dict.get("entry_timestamp"):
            if filter_dict["entry_timestamp"]["start_date"]:
                start_date = filter_dict["entry_timestamp"]["start_date"]
            if filter_dict["entry_timestamp"]["end_date"]:
                end_date = filter_dict["entry_timestamp"]["end_date"]
        
        time_row = dbc.Row(dcc.DatePickerRange(id='range',
                           min_date_allowed=datetime.datetime(2020, 10, 1),
                           start_date_placeholder_text='From Any Date',
                           end_date_placeholder_text='To Any Date',
                           start_date=start_date,
                           end_date=end_date,
                           clearable=True,
                           minimum_nights=0), className = "gx-1", style = {"margin-bottom": "5px"})
        filters = [time_row, *filters]
    return filters
#-----------------------------------------------------------------------

def construct_title(filter_dict, graph_type, selected_demographic=None):
    
    filter_dict = {key:value for (key, value) in\
                   filter_dict.items() if value}
    
    category_dict = database_constants.DEMOGRAPHIC_CATEGORIES
    title = ""
    meal_sites = filter_dict.get("meal_site")
    if meal_sites:
        del filter_dict["meal_site"]

    if graph_type == "pie":

        if filter_dict:
            filter_string = construct_filter_string(filter_dict)
            title += filter_string
        
        title+="Diner Entries "
        
        if filter_dict.get("entry_timestamp"):
            title+=f"between {filter_dict['entry_timestamp']['start_date']} and {filter_dict['entry_timestamp']['end_date']} "

        if selected_demographic:
            title += f"by {category_dict[selected_demographic]}"

        # title += "Percentage "
        # if selected_demographic:
        #     title += f"distribution of <b>{category_dict[selected_demographic]}</b> among Diners "
        # else:
        #     title += "of Diners "

        # if filter_dict:
        #     title += "who are "
        #     filter_string = construct_filter_string(filter_dict)
        #     title += filter_string

        # title = "<br>".join(textwrap.wrap(title, width= 100))

        # if meal_sites:
        #     title+="<br>At "
        #     site_string = construct_site_string(meal_sites)
        #     title+=site_string
        # else:
        #     title+="<br>Across all Meal Sites"
        

    if graph_type == "bar":
        
        if filter_dict:
            filter_string = construct_filter_string(filter_dict)
            title += filter_string
        
        title+="Diner Entries "

        if filter_dict.get("entry_timestamp"):
            title+=f"between {filter_dict['entry_timestamp']['start_date']} and {filter_dict['entry_timestamp']['end_date']} "
        
        if selected_demographic:
            title += f"by {category_dict[selected_demographic]} and "

        title+="by Meal Site"

    if graph_type == "line":
        timestamp_filter = filter_dict.get("entry_timestamp")
        filter_dict_no_time = filter_dict
        if timestamp_filter:
            del filter_dict_no_time["entry_timestamp"]
        if filter_dict_no_time:
            filter_string = construct_filter_string(filter_dict_no_time)
            title += filter_string

        if timestamp_filter:
            print(timestamp_filter)
            title+=f"Diner Entries between {timestamp_filter['start_date']} and {timestamp_filter['end_date']} "
        else:
            title+="Diner Entries All-Time "

        title+="by Meal Service Date"

        if selected_demographic == "Split":
            title+= " and by Meal Site"
            
    title = "<br>".join(textwrap.wrap(title, width=100))
    return title

# -----------------------------------------------------------------------

def construct_filter_string(filter_dict):
    status_options = database_constants.STATUS_OPTION_MAPPING
    
    filter_dict = {key:value for (key, value) in\
                   filter_dict.items() if value}

    if filter_dict.get("meal_site"):
        del filter_dict["meal_site"]
        
    if filter_dict.get("entry_timestamp"):
        del filter_dict["entry_timestamp"]


    filter_text_list = []
    filter_text_dict = {key:[] for (key, value) in filter_dict.items()}
    
    for key, value_list in filter_dict.items():
        for value in value_list:
            if key == "language":
                if value == "ASL":
                    filter_text_dict[key].append(f"{value}-speaking")
                else:
                    filter_text_dict[key].append(f"{value.title()}-speaking")
            elif key == "age_range":
                filter_text_dict[key].append(f"{value} years old")
            elif key == "zip_code":
                if value == "Unknown":
                    filter_text_dict[key].append(f"living at Unknown Zip Code")
                elif value == "Other":
                    filter_text_dict[key].append(f"living at Out-of-Area Zip Code")
                else:
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
    elif len(filter_text_list) == 1:
        filter_string = filter_text_list[0] + " "
    else:
        filter_string = ""

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

#-----------------------------------------------------------------------

def construct_slice_title(filter_dict):
    timestamp_filter = filter_dict.get("entry_timestamp")
    slice_title = construct_filter_string(filter_dict=filter_dict)
    
    if timestamp_filter:
        if slice_title:
            slice_title+=", "
        slice_title+= f"{timestamp_filter['start_date']} to {timestamp_filter['end_date']}"

    slice_title = slice_title.strip()
    slice_title = "<br>".join(textwrap.wrap(slice_title, width=45))
    return slice_title

#-----------------------------------------------------------------------

def graph_message(message_text):
    message = go.Figure()
    message.update_layout(
                        xaxis={"visible": False},
                        yaxis={"visible": False},
                        annotations=[
                            {
                                "text": message_text,
                                        "xref": "paper",
                                        "yref": "paper",
                                        "showarrow": False,
                                        "font": {
                                            "size": 28,
                                            "family": "Nunito",
                                            "color": "#6b6b6b"
                                        }
                            }
                        ]
                    )
    return message

#-----------------------------------------------------------------------

def old_filter_options_helper(selected_demographic, filter_dict):

    filters = []
    dem_row1 = []
    dem_row2 = []
    dem_row3 = []
    status_row1 = []
    status_row2 = []
    demographic_categories = database_constants.DEMOGRAPHIC_CATEGORIES

    for demographic_option in database_constants.DEMOGRAPHIC_OPTIONS:
        if demographic_option != selected_demographic:
            options_string = demographic_option.upper() + "_OPTIONS"
            # American Indian/Alaska Native
            # and Native Hawaiian/Pacific Islander
            # are too tall to fit in the default dropdown option height
            if demographic_option == "race":
                options_string = "RACE_DROPDOWN_OPTIONS"
            elif demographic_option == "zip_code":
                options_string = "ZIP_CODE_DROPDOWN_OPTIONS"
            
            height = 35

            if demographic_option in filter_dict.keys():
                if demographic_option in list(database_constants.STATUS_OPTION_MAPPING.keys()):
                    if demographic_option in ("homeless", "veteran"):
                        status_row1.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                                clearable=True,
                                                optionHeight=height,
                                                multi=True,
                                                value=filter_dict[demographic_option],
                                                placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    else:
                        status_row2.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                                clearable=True,
                                                optionHeight=height,
                                                multi=True,
                                                value=filter_dict[demographic_option],
                                                placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                else:
                    if demographic_option == "race":
                        dem_row1.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                                clearable=True,
                                                optionHeight=height,
                                                multi=True,
                                                value=filter_dict[demographic_option],
                                                placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    elif demographic_option in ("language", "age_range"):
                        dem_row2.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                                clearable=True,
                                                optionHeight=height,
                                                multi=True,
                                                value=filter_dict[demographic_option],
                                                placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    else:
                        dem_row3.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                                clearable=True,
                                                optionHeight=height,
                                                multi=True,
                                                value=filter_dict[demographic_option],
                                                placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    
                        
            else:
                if demographic_option in list(database_constants.STATUS_OPTION_MAPPING.keys()):
                    if demographic_option in ("homeless", "veteran"):
                        status_row1.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                    clearable=True,
                                    multi=True,
                                    value='',
                                    optionHeight=height,
                                    placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    else:
                        status_row2.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                    clearable=True,
                                    multi=True,
                                    value='',
                                    optionHeight=height,
                                    placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                else:
                    if demographic_option == "race":
                        dem_row1.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                    clearable=True,
                                    multi=True,
                                    value='',
                                    optionHeight=height,
                                    placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    elif demographic_option in ("language", "age_range"):
                        dem_row2.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                    clearable=True,
                                    multi=True,
                                    value='',
                                    optionHeight=height,
                                    placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                    else:
                        dem_row3.append(
                            dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                    'name': demographic_option},
                                                options=[{'value': o, 'label': o} for o in getattr(
                                                    database_constants, options_string)],
                                    clearable=True,
                                    multi=True,
                                    value='',
                                    optionHeight=height,
                                    placeholder="Any " + demographic_categories[demographic_option]
                                                )))
                
    dem_row1 = dbc.Row(dem_row1, className="gx-1", style = {"margin-bottom": "5px"})
    dem_row2 = dbc.Row(dem_row2, className="gx-1", style = {"margin-bottom": "5px"})
    dem_row3 = dbc.Row(dem_row3, className="gx-1", style = {"margin-bottom": "5px"})
    status_row1 = dbc.Row(status_row1, className="gx-1", style = {"margin-bottom": "5px"})
    status_row2 = dbc.Row(status_row2, className="gx-1", style = {"margin-bottom": "5px"})
    if dem_row1.children:
        filters = [dem_row1, dem_row2, dem_row3, status_row1, status_row2]   
    else:
        filters = [dem_row2, dem_row3, status_row1, status_row2]   
              
    return filters
#-----------------------------------------------------------------------