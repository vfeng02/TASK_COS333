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
import datetime
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

def init_linedashboard(server):
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
                                    min_date_allowed=datetime.datetime(1995, 8, 5),
                                    max_date_allowed=datetime.datetime(2022, 12, 31),
                                    start_date=datetime.datetime(2022, 10, 1),
                                    end_date=datetime.datetime(2022, 11, 13),
                             clearable=True,
                             
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
                html.H5("If Separate is selected, each selected meal site will get its own line on the graph"),
                dcc.RadioItems(id = 'site_grouping',
                               options = ['Group', 'Separate'],
                               value = 'Group',
                               inline=True),
                html.H4("Select Filters"),
                dbc.Row(id="filter_options", children=helpers.filter_options_helper(None, {}))

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
    
    @line_app.callback(
            Output('line_graph', 'figure'),
            [Input('range', 'start_date'),
             Input('range', 'end_date'),
             Input('site_options', 'value'),
             Input('site_grouping', 'value'),
             Input({'type': 'graph_filter', 'name': dash.ALL}, 'value')]

    )
    def update_line_graph(time_range_start, time_range_end, selected_sites, selected_grouping, selected_filters):
        selected_fields = helpers.selected_fields_helper(dash.callback_context.inputs)
        
        filter_dict = dict(zip(selected_fields, selected_filters))
        filter_dict["entry_timestamp"] = {"start_date": time_range_start, "end_date": time_range_end}
        selected_fields.append("entry_timestamp")
        selected_fields.append("meal_site")
        
        if selected_grouping == "Group":
        
            if selected_sites:
                filter_dict["meal_site"] = selected_sites
                selected_sites_data = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields)
                selected_sites_data = selected_sites_data.sort_values(by=["entry_timestamp"])
                line_graph = go.Figure(data = [go.Scatter(x = selected_sites_data["entry_timestamp"].dt.date.unique(), y=list(selected_sites_data.groupby(selected_sites_data["entry_timestamp"].dt.date)["entry_timestamp"].count()), mode = "lines+markers")])
                line_graph.update_layout(title="Change Over Time of the Amount of Diners with Selected Filters at Selected Meal Sites (Grouped)",
                                         xaxis_title = "dates",
                                         yaxis_title = "count")
                return line_graph

            else:
                all_sites_data =demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields)
                all_sites_data = all_sites_data.sort_values(by=["entry_timestamp"])
                all_line_graph = go.Figure(data = [go.Scatter(x = all_sites_data["entry_timestamp"].dt.date.unique(), y=list(all_sites_data.groupby(all_sites_data["entry_timestamp"].dt.date)["entry_timestamp"].count()), mode = "lines+markers")])
                all_line_graph.update_layout(title="Change Over Time of the Amount of Diners with Selected Filters at All Meal Sites (Grouped)",
                                         xaxis_title = "dates",
                                         yaxis_title = "count")
                return all_line_graph
        else:
            if selected_sites:
                filter_dict["meal_site"] = selected_sites
                selected_sites_data = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields)
                selected_sites_data = selected_sites_data.sort_values(by=["entry_timestamp"])
                # split df into df by meal site, add trace for each meal site
                sites_dict = {elem: pandas.DataFrame() for elem in selected_sites_data["meal_site"].unique()}
                line_graph = go.Figure()
                for key in sites_dict.keys():
                    sites_dict[key] = selected_sites_data[:][selected_sites_data.meal_site == key]
                    line_graph.add_trace(go.Scatter(x = sites_dict[key]["entry_timestamp"].dt.date.unique(), y=list(sites_dict[key].groupby(sites_dict[key]["entry_timestamp"].dt.date)["entry_timestamp"].count()), mode = "lines+markers"))
                line_graph.update_layout(title="Change Over Time of the Amount of Diners with Selected Filters at Selected Meal Sites (Separate)",
                                         xaxis_title = "dates",
                                         yaxis_title = "count",
                                         )
                return line_graph

            else:
                selected_sites_data = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields)
                selected_sites_data = selected_sites_data.sort_values(by=["entry_timestamp"])
                # split df into df by meal site, add trace for each meal site
                sites_dict = {elem: pandas.DataFrame() for elem in selected_sites_data["meal_site"].unique()}
                all_line_graph = go.Figure()
                for key in sites_dict.keys():
                    sites_dict[key] = selected_sites_data[:][selected_sites_data.meal_site == key]
                    all_line_graph.add_trace(go.Scatter(x = sites_dict[key]["entry_timestamp"].dt.date.unique(), y=list(sites_dict[key].groupby(sites_dict[key]["entry_timestamp"].dt.date)["entry_timestamp"].count()), mode = "lines+markers"), name = key)
                all_line_graph.update_layout(title="Change Over Time of the Amount of Diners with Selected Filters Across All Meal Sites (Separate)",
                                         xaxis_title = "dates",
                                         yaxis_title = "count")
                return all_line_graph
            