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
                html.H4(
                "Select Meal Sites (Clear Selections to Show All Sites)"),
                html.H5("Selected sites will each have their own bar(s) on the graph"),
                dcc.Dropdown(id='site_options',
                             options=[{'value': o, 'label': o}
                                 for o in database_constants.MEAL_SITE_OPTIONS],
                             clearable=True,
                             multi=True,
                             value=["First Baptist Church",
                                 "Trenton Area Soup Kitchen"]
                             ),
                html.H4("Select a Demographic Category"),
                dcc.Dropdown(id='demographic',
                             options= [{"label": option.replace("_", " ").title(), "value": option}
                                       for option in database_constants.DEMOGRAPHIC_OPTIONS],
                             clearable=True,
                             value='gender'
                             ),
                html.H4("Select Filters"),
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
                selected_sites_df = demographic_db.get_patrons(
                        filter_dict=filter_dict, select_fields=selected_fields)
                histogram = px.histogram(selected_sites_df, x=selected_demographic,
                color='meal_site', barmode='group', title=f"Comparison of {selected_demographic} of Diners at Selected Meal Sites")
                return histogram
            else:
                all_site_data = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields)
                all_histogram = px.histogram(all_site_data, x=selected_demographic,
                color='meal_site', barmode='group',
                title = f"Comparison of {selected_demographic.title()} of Diners at All Meal Sites")
                return all_histogram

        elif selected_filters:

            if selected_sites:
                filter_dict["meal_site"] = selected_sites
                selected_sites_data = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields).groupby("meal_site")["entry_timestamp"].count()
                selected_sites_data.rename("count", inplace=True)
                bar_graph = px.bar(selected_sites_data, x = selected_sites_data.index,\
                                    y = "count", title = "Comparison of Diners With Selected Filters At Selected Meal Sites", text_auto = True,
                                    color=selected_sites_data.index)
                bar_graph.update_layout(showlegend=False)
                return bar_graph
                
            else:
                all_site_data = demographic_db.get_patrons(
                                filter_dict=filter_dict, select_fields=selected_fields).groupby("meal_site")["entry_timestamp"].count()
                all_site_data.rename("count", inplace=True)
                all_bar_graph = px.bar(all_site_data, x = all_site_data.index,\
                                    y = "count", title = "Comparison of Diners With Selected Filters Across All Meal Sites", text_auto = True,
                                    color = all_site_data.index)
                all_bar_graph.update_layout(showlegend=False)
                return all_bar_graph




            
            
