#!/usr/bin/env python

#-----------------------------------------------------------------------
# piedashboard.py
# Author: Andres Blanco Bonilla
# Dash app for pie chart display
# route: /pieapp
#-----------------------------------------------------------------------

"""Instantiate a Dash app."""
import dash
import pandas
from TASKdbcode import demographic_db
from TASKdbcode import database_constants
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify as di
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from TASKdbcode import graphdashboard_helpers as helpers
import textwrap

def init_piedashboard(server):
    pie_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/pieapp/",
        # using default bootstrap style sheet, could be changed
        external_stylesheets=[dbc.themes.BOOTSTRAP])

    pie_app.layout = html.Div(
        children=[
            html.Div(children=[
                html.Div([
                        html.H4("Select Meal Sites", style={'display': 'inline-block', 'margin-right': '5px'}), 
                        di(icon = "material-symbols:help-outline-rounded", id="mshelp", color = "194f77", inline = True, height = 20),
                        dbc.Tooltip([html.P("Select the meal sites whose entries you want to be included in the pie chart. Data from your selected meal sites will be grouped together into one single pie chart. Clear your selection to automatically select any/all meal sites.",
                                            style = {"textAlign": "left", "marginBottom": 0})], target = "mshelp", style = {"width": 600}),
                        html.H5("Compile data from diners at...")]),
                dcc.Dropdown(id='site_options',
                             options=[{'value': o, 'label': o}
                                 for o in database_constants.MEAL_SITE_OPTIONS],
                             clearable=True,
                             multi=True,
                             value=["First Baptist Church"],
                             placeholder = "All Meal Sites",
                             ),   
                html.Div([
                        html.H4("Select Filters on Diners", style={'display': 'inline-block', 'margin-right': '5px'}), 
                        di(icon = "material-symbols:help-outline-rounded", id="fhelp", color = "194f77", inline = True, height = 20),
                        dbc.Tooltip([html.P("The pie chart will only include data from diners who meet the criteria of all your selected filters. Clear a filter selection to automatically include any/all options of that category.",
                                            style = {"textAlign": "left", "marginBottom": 0})], target = "fhelp", style = {"width": 600})]),
                html.H5("Make a chart of diners who are..."),
                dbc.Row(id="filter_options", children=[]),
                html.Div([
                        html.H4("Select Demographic Category to Show Percentage Distribution", style={'display': 'inline-block', 'margin-right': '5px'}), 
                        di(icon = "material-symbols:help-outline-rounded", id="dchelp", color = "194f77", inline = True, height = 20),
                        dbc.Tooltip([html.P("Break down diner data by the category you select. For example, selecting Veteran Status will create slices for Veteran, Not a Veteran, and Unknown on the pie chart.",
                                            style = {"textAlign": "left", "marginBottom": 0})], target = "dchelp", style = {"width": 600}),
                        html.H5("Break down diners by...")]),
                dcc.Dropdown(id='demographic',
                             options= [{"label": label, "value": value}
                                       for label, value in zip(database_constants.DEMOGRAPHIC_CATEGORY_DROPDOWN_LABELS,
                                                               database_constants.DEMOGRAPHIC_CATEGORY_DROPDOWN_VALUES)],
                             clearable=False,
                             value='gender'
                             ),      

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

        # overall, would be great if the title of the charts were clearer
        # kinda hard to understand what exactly you're looking at atm lol
        
        # to do for pie charts:
        # change colors to be readable in black and white and less ugly
        
        # fix scrolling and iframe, there's like 4 overlapping scrollbars
        # and it looks hideous lol, may need to mess with the iframe
        # size and page layout
        # ideally, the chart section doesn't have its own scrollbar
        # and it just scrolls with the rest of the page
        
        # There is also an issue where the chart completely disappears
        # if you select a demographic category and filters,
        # and no diner fits all those filters,
        # or if you select no demographic category,
        # with no filters
        # there should be something less ugly than just a blank space
        
        if selected_demographic:

            selected_fields.append(selected_demographic)

            if selected_sites:
                filter_dict["meal_site"] = selected_sites
                
            diner_data_df = demographic_db.get_patrons(
                        filter_dict=filter_dict, select_fields=selected_fields)
            num_entries = len(diner_data_df.index)
            percent_labels = [f"{option}: {value/num_entries:.2%}"\
                                 for option, value in zip(
                                 diner_data_df[selected_demographic]\
                                 .value_counts().index.tolist(),\
                                 list(diner_data_df[selected_demographic].value_counts()))]
            pie_chart=go.Figure(data=[go.Pie(labels=percent_labels,
                                                 values=list(diner_data_df[selected_demographic].value_counts()),
                                                 texttemplate="%{label}<br>(%{value} Entries)")])
            pie_chart_title = helpers.construct_title(filter_dict, graph_type="pie", selected_demographic=selected_demographic)
            pie_chart.update_layout(title=pie_chart_title)
            pie_chart.update_traces(textposition='inside')
            pie_chart.update_layout(uniformtext_minsize=9, uniformtext_mode='hide')
            return pie_chart

        else:

            if selected_sites:
                filter_dict["meal_site"] = selected_sites
                num_entries = demographic_db.get_num_entries(selected_sites)
            else:
                num_entries = demographic_db.get_total_entries()

            diner_data = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields)["entry_timestamp"].count()
            num_other_entries = num_entries - diner_data
            filtered_slice_title = helpers.construct_filter_string(filter_dict=filter_dict).strip()
            filtered_slice_title = "<br>".join(textwrap.wrap(filtered_slice_title, width=50))
            diner_data = pandas.Series([diner_data],[filtered_slice_title])
            other_count = pandas.Series([num_other_entries], ["Other"])
            diner_data = pandas.concat([diner_data, other_count])
            percent_labels = [f"{option}: {value/num_entries:.2%}" for option, value in zip(diner_data.index, diner_data.values)]
            exp_pie_chart = go.Figure(data = [go.Pie(labels = percent_labels, values = diner_data.values, texttemplate = "%{label}<br>(%{value} Entries)", pull = [0.2,0], rotation = 295)])
            exp_pie_chart_title = helpers.construct_title(filter_dict, graph_type = "pie", selected_demographic=selected_demographic)
            exp_pie_chart.update_layout(title = exp_pie_chart_title)                    
            return exp_pie_chart
