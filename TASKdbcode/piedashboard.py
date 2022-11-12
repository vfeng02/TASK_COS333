#!/usr/bin/env python

#-----------------------------------------------------------------------
# piedashboard.py
# Author: Andres Blanco Bonilla
# dash app for pie charts
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


def init_piedashboard(server):
    pie_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/pieapp/",
        external_stylesheets=[dbc.themes.BOOTSTRAP])

    df = demographic_db.get_patrons()
    demographic_options = []
    for option in database_constants.DEMOGRAPHIC_OPTIONS:
        demographic_options.append(
            {"label": option.title(), "value": option})

    pie_app.layout = html.Div(
        children=[
            html.Div(children=[
                html.H4(
                    "Select Meal Sites (Clear Selections to Show All Sites)"),
                html.H5("Data from selected sites will be aggregated together into a single pie chart"),
                dcc.Dropdown(id='site_options',
                             options=[{'value': o, 'label': o}
                                 for o in database_constants.MEAL_SITE_OPTIONS],
                             clearable=True,
                             multi=True,
                             value=["First Baptist Church"]
                             ),
                html.H4("Select a Demographic"),
                dcc.Dropdown(id='demographic',
                             options=demographic_options,
                             clearable=True,
                             value='gender'
                             )         
                , html.H4("Select Filters"),
                dbc.Row(id="filter_options", children=[]),

            ], className='menu-l'
            ),
            dcc.Graph(id='pie_chart',
                      config={'displayModeBar': True,
                          'displaylogo': False},
                      className='card',
                      style={'width': '100vw', 'height': '100vh'}
                      )
        ]
    )

    init_callbacks(pie_app)
    pie_app.enable_dev_tools(
    dev_tools_ui=True,
    dev_tools_serve_dev_bundles=True,)

    return pie_app.server

def init_callbacks(pie_app):

    @pie_app.callback(
            Output('filter_options', 'children'),
            Input('demographic', 'value'),
            State({'type': 'graph_filter', 'name': dash.ALL}, 'value')
    )
    def update_filter_options(selected_demographic, selected_filters):
        selected_fields = helpers.selected_fields_helper(dash.callback_context.states)
        filter_dict = dict(zip(selected_fields, selected_filters))
        filters = helpers.filter_options_helper(selected_demographic, filter_dict)
        return filters

    @pie_app.callback(
            Output('pie_chart', 'figure'),
            [Input('site_options', 'value'),
            Input('demographic', 'value'),
            Input({'type': 'graph_filter', 'name': dash.ALL}, 'value')]
    )
    def update_pie_chart(selected_sites, selected_demographic, selected_filters):
        selected_fields = helpers.selected_fields_helper(dash.callback_context.inputs)
        filter_dict = dict(zip(selected_fields, selected_filters))
        selected_fields.append("entry_timestamp")
        #print(site_df)
        if selected_demographic:
            selected_fields.append(selected_demographic)
            if selected_sites:
                site_dfs = []
                for site in selected_sites:
                    site_filter_dict = filter_dict
                    site_filter_dict["meal_site"] = site
                    site_dfs.append(demographic_db.get_patrons(
                        filter_dict=site_filter_dict, select_fields=selected_fields))
                combined_df = pandas.concat(site_dfs)
                pie_chart=go.Figure(data=[go.Pie(labels=combined_df[selected_demographic].value_counts().index.tolist(),
                                                 values=list(combined_df[selected_demographic].value_counts()))])
                pie_chart.update_layout(title=
                f"Distribution of {selected_demographic.title()} of Diners at Selected Sites")
                return pie_chart
            else:
                all_site_df = demographic_db.get_patrons(filter_dict = filter_dict)
                all_pie_chart=go.Figure(data=[go.Pie(labels=all_site_df[selected_demographic].value_counts().index.tolist(),
                                                 values=list(all_site_df[selected_demographic].value_counts()))])
                all_pie_chart.update_layout(title=
                f"Distribution of {selected_demographic.title()} of Diners at All Sites")
                return all_pie_chart
        else: 
            if selected_sites:
                site_dfs = []
                for site in selected_sites:
                    site_filter_dict = filter_dict
                    site_filter_dict["meal_site"] = site
                    site_dfs.append(demographic_db.get_patrons(
                        filter_dict=site_filter_dict, select_fields=selected_fields))
                combined_data = pandas.concat(site_dfs)["entry_timestamp"].count()
                num_entries = len(site_dfs) * 50
                num_entries = num_entries - combined_data
                combined_data = pandas.Series([combined_data],["Diners with Selected Filters"])
                other_count = pandas.Series([num_entries], ["Other"])
                combined_data = pandas.concat([combined_data, other_count])
                exp_pie_chart = go.Figure(data = [go.Pie(values = combined_data.values, labels = combined_data.index, pull = [0.2,0],
                                                         title = "Percentage of Diners with Selected Filters at Selected Meal Site")])
                return exp_pie_chart
            else:
                all_site_data = demographic_db.get_patrons(
                                filter_dict=filter_dict, select_fields=selected_fields)["entry_timestamp"].count()
                num_entries = len(database_constants.MEAL_SITE_OPTIONS) * 50
                num_entries = num_entries - all_site_data
                all_site_data = pandas.Series([all_site_data],["Diners with Selected Filters"])
                other_count = pandas.Series([num_entries], ["Other"])
                all_site_data = pandas.concat([all_site_data, other_count])
                all_exp_pie_chart = go.Figure(data = [go.Pie(values = all_site_data.values, labels = all_site_data.index, pull = [0.2,0],
                                          title = "Percentage of Diners with Selected Filters Across All Meal Sites")])
                return all_exp_pie_chart
                
                
        