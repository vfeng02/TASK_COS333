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
from dash_iconify import DashIconify as di
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from TASKdbcode import graphdashboard_helpers as helpers

GOOGLE_FONTS = "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0"
CUSTOM_BOOTSTRAP = '../static/custombootstrap.min.css'

def init_linedashboard(server):
    line_app = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix="/lineapp/",
        external_stylesheets=[CUSTOM_BOOTSTRAP, GOOGLE_FONTS])

    demographic_options = []
    for option in database_constants.DEMOGRAPHIC_OPTIONS:
        demographic_options.append(
            {"label": option.replace("_", " ").title(), "value": option})

    line_app.layout = html.Div(
        children=[
            dbc.Container([
            dbc.Row([
            dbc.Col([
            html.H3("Graph by Date", style = {'color':'#ffc88f', 'margin-top':'5px', 'font-weight':'bold'}),
            html.Div([
                html.Hr(style={"width": "100%", 'borderTop': '3px solid #ff911f','borderBottom': '2px #ff911f',"opacity": "unset"}),
                 html.Div([
                        html.H4("Select Date Range", style={'display': 'inline-block', 'margin-right': '5px', 'color':'white'}), 
                        di(icon = "material-symbols:help-outline-rounded", id="drhelp", color = "white", inline = True, height = 20),
                        dbc.Tooltip([html.P("A line graph will be constructed with the data from the dates in the range you select. Includes start date and end date.",
                                            style = {"textAlign": "left", "marginBottom": 0})], target = "drhelp", style = {"width": 600}),
                        html.H5("View data between the dates of...", style = {"color":"white"})]),
                dcc.DatePickerRange(id='range',
                                    min_date_allowed=datetime.datetime(2021, 10, 1),
                                    start_date=datetime.date(2021, 10, 1),
                                    end_date=datetime.date.today(),
                                    start_date_placeholder_text = "Earliest Date",
                                    end_date_placeholder_text = "Latest Date",
                                    clearable=True,
                                    minimum_nights=0
                             ),
                html.Div([
                    html.Hr(style={"width": "100%", 'borderTop': '3px solid #ff911f','borderBottom': '2px #ff911f',"opacity": "unset"}),
                    html.H4("Select Meal Sites", style={
                            'display': 'inline-block', 'margin-right': '5px','color': 'white'}),
                    di(icon="material-symbols:help-outline-rounded",
                       id="mshelp", color="white", inline=True, height=20),
                    dbc.Tooltip([html.P("Select the meal sites whose entries you want to be included in the line graph. Clear your selection to automatically select any/all meal sites.",
                                        style={"textAlign": "left", "marginBottom": 0})], target="mshelp", style={"width": 600}),
                    html.H5("Compile or Compare data from diners at...", style = {"color":"white"})]),
                dcc.Dropdown(id='site_options',
                             options=[{'value': o, 'label': o}
                                      for o in database_constants.MEAL_SITE_OPTIONS],
                             clearable=True,
                             multi=True,
                             value=["Trenton Area Soup Kitchen"],
                             placeholder="All Meal Sites"
                             ),
                html.Div([
                        html.H4("Group/Split Meal Site Data", style={'display': 'inline-block', 'margin-right': '5px', 'margin-top':'5px', 'color':'white'}), 
                        di(icon = "material-symbols:help-outline-rounded", id="gshelp", color = "white", inline = True, height = 20),
                        dbc.Tooltip([html.P("If Group is selected, data from your selected meal sites will be grouped together into one single line on the graph.", style = {"textAlign": "left"}),
                                     html.P("If Split is selected, each of your selected meal sites will get its own line on the graph.",
                                            style = {"textAlign": "left", "marginBottom": 0})], target = "gshelp", style = {"width": 600})]),
                dbc.RadioItems(id = 'site_grouping',
                               options=[
                               {"label": "Group", "value": "Group"},
                               {"label": "Split", "value": "Split"}],
                               value = 'Group',
                               inline=True,
                               style = {'color':'white'}),
                html.Hr(style={"width": "100%", 'borderTop': '3px solid #ff911f','borderBottom': '2px #ff911f',"opacity": "unset"}),
                html.Div([
                    html.H4("Select Filters on Diners", style={
                            'display': 'inline-block', 'margin-right': '5px'}),
                    di(icon="material-symbols:help-outline-rounded",
                       id="fhelp", color="white", inline=True, height=20),
                    dbc.Tooltip([html.P("The line graph will only include data from diners who meet the criteria of all your selected filters. Clear a filter selection to automatically include any/all options of that category.",
                                        style={"textAlign": "left", "marginBottom": 0})], target="fhelp", style={"width": 600}),
                ], style={'color': 'white'}),
                html.H5("Make a graph of diners who are...",style={'color': 'white'}),
                dbc.Row(id="filter_options", children=helpers.filter_options_helper(None, {}, "line")),
                html.Hr(style={"width": "100%", 'borderTop': '3px solid #ff911f','borderBottom': '2px #ff911f',"opacity": "unset"}),

            ], className='menu-l'
            )], width = 4),
            dbc.Col([
            dcc.Graph(id='line_graph',
                      className = 'card',
                      config={'displayModeBar': True,
                              'displaylogo': False},
                      style={'width': '100%', 'height': '100%',
                             'display':'block'}
                      )], width = 8),
        ])], fluid = True)],style = {'display':'block', 'background-color': '#145078',
                                   'height':'100vh', 'width':'100%'}
    )

    init_callbacks(line_app)

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
        time_filter = {}
        if time_range_start:
            time_filter["start_date"] = time_range_start
        else:
            time_filter["start_date"] = datetime.date(2022, 10, 1)

        if time_range_end:
            time_filter["end_date"] = time_range_end
        else:
            time_filter["end_date"] = datetime.date.max

        if time_range_start or time_range_end:
            filter_dict["entry_timestamp"] = time_filter

        selected_fields.append("entry_timestamp")
        selected_fields.append("meal_site")
        
        if selected_grouping == "Group":
        
            if selected_sites:
                filter_dict["meal_site"] = selected_sites
            diner_data_df = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields)
            if len(diner_data_df.index) == 0:
                    none_found_message = helpers.graph_message("No entries found.")
                    return none_found_message
            diner_data_df = diner_data_df.sort_values(by=["entry_timestamp"])
            if time_range_start and not time_range_end:
                    filter_dict['entry_timestamp']['end_date'] = diner_data_df['entry_timestamp'].tail(1).item().date()
            line_graph_title = helpers.construct_title(filter_dict=filter_dict, graph_type="line", selected_demographic=selected_grouping)
            line_graph = go.Figure(data = [go.Scatter(x = diner_data_df["entry_timestamp"].dt.date.unique(), y=list(diner_data_df.groupby(diner_data_df["entry_timestamp"].dt.date)["entry_timestamp"].count()), mode = "lines+markers")])
            line_graph.update_layout(title=line_graph_title,
                                         xaxis_title = "dates",
                                         yaxis_title = "number of entries")
            return line_graph

        else:

            if selected_sites:
                filter_dict["meal_site"] = selected_sites
            diner_data_df = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields)
            if len(diner_data_df.index) == 0:
                    none_found_message = helpers.graph_message("No entries found.")
                    return none_found_message
            diner_data_df = diner_data_df.sort_values(by=["entry_timestamp"])
            if time_range_start and not time_range_end:
                    filter_dict['entry_timestamp']['end_date'] = diner_data_df['entry_timestamp'].tail(1).item().date()
            # split df into df by meal site, add trace for each meal site
            sites_dict = {elem: pandas.DataFrame() for elem in diner_data_df["meal_site"].unique()}
            line_graph = go.Figure()
            line_graph_title = helpers.construct_title(filter_dict=filter_dict, graph_type="line", selected_demographic=selected_grouping)
            for key in sites_dict.keys():
                sites_dict[key] = diner_data_df[:][diner_data_df.meal_site == key]
                line_graph.add_trace(go.Scatter(x = sites_dict[key]["entry_timestamp"].dt.date.unique(), y=list(sites_dict[key].groupby(sites_dict[key]["entry_timestamp"].dt.date)["entry_timestamp"].count()), mode = "lines+markers", name = key))
            line_graph.update_layout(title=line_graph_title,
                                         xaxis_title = "dates",
                                         yaxis_title = "number of entries",
                                         )
            return line_graph
            