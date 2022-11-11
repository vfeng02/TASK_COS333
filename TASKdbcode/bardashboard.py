#!/usr/bin/env python

#-----------------------------------------------------------------------
# bardashboard.py
# Author: Andres Blanco Bonilla
# dash app for bar graphs
#-----------------------------------------------------------------------

"""Instantiate a Dash app."""
import dash
import pandas
from TASKdbcode import demographic_db
from TASKdbcode import database_constants
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go


def init_bardashboard(server):
    bar_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/barapp/",
        external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    df = demographic_db.get_patrons()
    demographic_options = []
    for option in database_constants.DEMOGRAPHIC_OPTIONS:
        demographic_options.append({"label": option.title(), "value": option})


    bar_app.layout = html.Div(
        children=[
            html.Div(children=[
                html.H4("Select a Demographic"),
                dcc.Dropdown(id='demographic',
                             options=demographic_options,
                             clearable=True,
                             value='race'
                             )
                # maybe make this hover text or something? I really don't know how this should look
                , html.H4("And/Or Select Filters (If no demographic is selected, your filters will be compared across all meal sites"),
                dbc.Row(id = "filter_options", children = []),
                html.Div(id = "site_selection", children = [
                html.H4("Select Meal Sites (recommended max 4. you could select more than 4, but your bar graph might look ugly)"),
                dcc.Dropdown(id = 'site_options',                             
                             options= [{'value': o, 'label': o} for o in database_constants.MEAL_SITE_OPTIONS],
                             clearable=True,
                             multi = True,
                             value=["First Baptist Church", "Trenton Area Soup Kitchen"]
                             )
                    
                ])
            ], className='menu-l'
            ),
            dcc.Graph(id='interaction2',
                      config={'displayModeBar': True, 'displayLogo': False},
                      className='card',
                      style = {'width': '100vw', 'height': '100vh'}
                      )
        ]
    )
    
    init_callbacks(bar_app)

    return bar_app.server



def init_callbacks(bar_app):
    
    @bar_app.callback(
            Output('filter_options', 'children'),
            Input('demographic', 'value')
    )
    def update_filter_options(selected_demographic):
        filters = []
        for demographic_option in database_constants.DEMOGRAPHIC_OPTIONS:
            if demographic_option != selected_demographic:
                options_string = demographic_option.upper() + "_OPTIONS"
                filters.append(
                    dbc.Col(dcc.Dropdown(id = {'type': 'graph_filter',
                                               'name': demographic_option},
                             options=[{'value': o, 'label': o} for o in getattr(database_constants, options_string)],
                             clearable=True,
                             value='',
                             placeholder= demographic_option.replace("_", " ").title() + "..."
                             ))
                    )
        return filters
    


    @bar_app.callback(
            Output('site_selection', 'hidden'),
            [Input('demographic', 'value')]
    )
    def hide_site_options(selected_demographic):
        if not selected_demographic:
            return True
        else:
            return False
            
        
        
    
    @bar_app.callback(
            Output('interaction2', 'figure'),
            [Input('site_options', 'value'),
            Input('demographic', 'value'),
            Input({'type': 'graph_filter', 'name': dash.ALL}, 'value')]
        # B) defining the callback and what to return here
    )
    def update_bar_graph(selected_sites, selected_demographic, selected_filters):
        selected_fields = list(dash.callback_context.inputs.keys())
        selected_fields.pop(0)
        selected_fields.pop(0)
        selected_fields = [eval(field.strip(".value")) for field in selected_fields]
        selected_fields = [field["name"] for field in selected_fields]
        filter_dict = dict(zip(selected_fields, selected_filters))
        selected_fields.append("meal_site")
        selected_fields.append("entry_timestamp")
        selected_fields.append(selected_demographic)
        
        if selected_sites:
            site_dfs = [] 
            for site in selected_sites:
                site_filter_dict = filter_dict
                site_filter_dict["meal_site"] = site
                site_dfs.append(demographic_db.get_patrons(filter_dict=site_filter_dict, select_fields=selected_fields))
            combined_df = pandas.concat(site_dfs)
            histogram = px.histogram(combined_df, x=selected_demographic,
            color='meal_site', barmode='group', title =\
                 f"Comparison of {selected_demographic} of Diners at Selected Meal Sites")
            return histogram
            
        else:
            all_site_data = demographic_db.get_patrons(\
                        filter_dict = filter_dict, select_fields\
                            = selected_fields).groupby("meal_site")\
                                ["entry_timestamp"].count()
            all_site_data.rename("count", inplace=True)
            bar_graph = px.bar(all_site_data, x = all_site_data.index,\
                              y = "count", title = "Comparison of Diners With Selected Filters Across All Meal Sites", text_auto = True)
            bar_graph.update_layout(showlegend=False)
            return bar_graph


            
            



