#!/usr/bin/env python

#-----------------------------------------------------------------------
# bardashboard.py
# Author: Andres Blanco Bonilla
# Dash app for bar graph display
# route: /barapp
#-----------------------------------------------------------------------

"""Instantiate a Dash app."""
import dash
import pandas
from TASKdbcode import demographic_db
from TASKdbcode import database_constants
from TASKdbcode import graphdashboard_helpers as helpers
from dash import dcc
from dash import html
from dash_iconify import DashIconify as di
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go


def init_bardashboard(server):
    bar_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/barapp/",
        # using the default bootstrap style sheet, could be changed
        external_stylesheets=[dbc.themes.BOOTSTRAP])

    bar_app.layout = html.Div(
        children=[
            html.Div(children=[
                html.Div([
                        html.H4("Select Meal Sites", style={'display': 'inline-block', 'margin-right': '5px'}), 
                        di(icon = "material-symbols:help-outline-rounded", id="mshelp", color = "194f77", inline = True, height = 20),
                        dbc.Tooltip([html.P("Select the meal sites whose data you want to be included in the bar graph. Each meal site will get its own bar (or set of bars) on the graph. Clear your selection to automatically select all meal sites.",
                                            style = {"textAlign": "left", "marginBottom": 0})], target = "mshelp", style = {"width": 600})]),
                dcc.Dropdown(id='site_options',
                             options=[{'value': o, 'label': o}
                                 for o in database_constants.MEAL_SITE_OPTIONS],
                             clearable=True,
                             multi=True,
                             value=["First Baptist Church",
                                 "Trenton Area Soup Kitchen"]
                             ),
                html.Div([
                        html.H4("Select a Demographic Category", style={'display': 'inline-block', 'margin-right': '5px'}), 
                        di(icon = "material-symbols:help-outline-rounded", id="dchelp", color = "194f77", inline = True, height = 20),
                        dbc.Tooltip([html.P("Break down diner data by the category you select. For example, selecting Veteran will create True, False, and Unknown sections on the bar graph.",
                                            style = {"textAlign": "left", "marginBottom": 0})], target = "dchelp", style = {"width": 600})]),
                dcc.Dropdown(id='demographic',
                             options= [{"label": option.replace("_", " ").title(), "value": option}
                                       for option in database_constants.DEMOGRAPHIC_OPTIONS],
                             clearable=True,
                             value='gender'
                             ),
                html.Div([
                        html.H4("Select Filters", style={'display': 'inline-block', 'margin-right': '5px'}), 
                        di(icon = "material-symbols:help-outline-rounded", id="fhelp", color = "194f77", inline = True, height = 20),
                        dbc.Tooltip([html.P("The bar graph will only include data from diners who meet the criteria of all your selected filters.",
                                            style = {"textAlign": "left", "marginBottom": 0})], target = "fhelp", style = {"width": 600})]),
                # the options for race look weird bc they're long
                dbc.Row(id="filter_options", children=[]),
            ], className='menu-l'
            ),
            dcc.Graph(id='bar_graph',
                      config={'displayModeBar': True,
                          'displaylogo': False},
                      className='card',
                      style={'width': '100vw', 'height': '100vh'}
                      )
        ]
    )



    init_callbacks(bar_app)
    bar_app.enable_dev_tools(
    dev_tools_ui=True,
    dev_tools_serve_dev_bundles=True,)

    return bar_app.server


def init_callbacks(bar_app):

    @bar_app.callback(
        Output('filter_options', 'children'),
        Input('demographic', 'value'),
        State({'type': 'graph_filter', 'name': dash.ALL}, 'value')
    )
    def update_filter_options(selected_demographic, selected_filters):
        selected_fields = helpers.selected_fields_helper(dash.callback_context.states)
        filter_dict = dict(zip(selected_fields, selected_filters))
        filters = helpers.filter_options_helper(selected_demographic, filter_dict)
        return filters


    @bar_app.callback(
            Output('bar_graph', 'figure'),
            [Input('site_options', 'value'),
            Input('demographic', 'value'),
            Input({'type': 'graph_filter', 'name': dash.ALL}, 'value')]

    )
    def update_bar_graph(selected_sites, selected_demographic, selected_filters):
        
        selected_fields = helpers.selected_fields_helper(dash.callback_context.inputs)
        filter_dict = dict(zip(selected_fields, selected_filters))
        selected_fields.append("entry_timestamp")
        selected_fields.append("meal_site")
        
        # The control flow of these if/else statements is logical,
        # but a little complicated
        # Maybe there is a cleaner way of arranging these chunks?

        # overall, would be great if the title of the graphs were clearer
        # kinda hard to understand what exactly you're looking at atm lol
        
        # to do for bar graphs:
        # colors repeat sometimes and it may be hard to read, need to change colors
        # maybe change display when no diners are found, it's not as bad as pie charts,
        # but still not great, some sort of "Not Found" message might be good
        if selected_demographic:
            
            selected_fields.append(selected_demographic)
            
            if selected_sites:
                filter_dict["meal_site"] = selected_sites
    
            diner_data_df = demographic_db.get_patrons(
                        filter_dict=filter_dict, select_fields=selected_fields)
            histogram_title = helpers.construct_title(filter_dict, graph_type="bar", selected_demographic=selected_demographic)
            histogram = px.histogram(diner_data_df, x=selected_demographic,
            color='meal_site', barmode='group', title=histogram_title, text_auto=True)
            histogram.update_layout(yaxis_title = "number of entries")
            return histogram

        else:

            if selected_sites:
                filter_dict["meal_site"] = selected_sites
                
            selected_sites_data = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields).groupby("meal_site")["entry_timestamp"].count()
            selected_sites_data.rename("number of entries", inplace=True)
            bar_graph_title = helpers.construct_title(filter_dict, graph_type="bar", selected_demographic=selected_demographic)
            bar_graph = px.bar(selected_sites_data, x = selected_sites_data.index,\
                                    y = "number of entries", title = bar_graph_title, text_auto = True,
                                    color=selected_sites_data.index)
            bar_graph.update_layout(showlegend=False)
            return bar_graph





            
            



