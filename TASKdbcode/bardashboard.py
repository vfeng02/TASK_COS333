#!/usr/bin/env python

# -----------------------------------------------------------------------
# bardashboard.py
# Author: Andres Blanco Bonilla
# dash app for bar graphs
# -----------------------------------------------------------------------

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


def init_bardashboard(server):
    bar_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/barapp/",
        external_stylesheets=[dbc.themes.BOOTSTRAP])

    df = demographic_db.get_patrons()
    demographic_options = []
    for option in database_constants.DEMOGRAPHIC_OPTIONS:
        demographic_options.append(
            {"label": option.title(), "value": option})

    bar_app.layout = html.Div(
        children=[
            html.Div(children=[
                html.H4("Select a Demographic"),
                dcc.Dropdown(id='demographic',
                             options=demographic_options,
                             clearable=True,
                             value='race'
                             )                # maybe make this hover text or something? I really don't know how this should look
                , html.H4("And/Or Select Filters"),
                dbc.Row(id="filter_options", children=[]),
                html.Div(id="site_selection", children=[
                html.H4(
                    "Select Meal Sites (Clear Selections to Show All Sites)"),
                dcc.Dropdown(id='site_options',
                             options=[{'value': o, 'label': o}
                                 for o in database_constants.MEAL_SITE_OPTIONS],
                             clearable=True,
                             multi=True,
                             value=["First Baptist Church",
                                 "Trenton Area Soup Kitchen"]
                             )

                ], style={'display': 'block'})
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
            [Input('demographic', 'value'),
            Input('site_options', 'value'),
            Input({'type': 'graph_filter', 'name': dash.ALL}, 'value')]
    )
    def update_filter_options(selected_demographic, selected_sites, selected_filters):
        
        triggered_component = dash.callback_context.triggered_id
        if triggered_component != "demographic":
            dash.exceptions.PreventUpdate
        selected_fields = list(dash.callback_context.inputs)
        selected_fields.pop(0)
        selected_fields.pop(0)
        selected_fields = [eval(field.strip(".value"))
                                for field in selected_fields]
        selected_fields = [field["name"] for field in selected_fields]
        
        filter_dict = dict(zip(selected_fields, selected_filters))

        filters = []
        for demographic_option in database_constants.DEMOGRAPHIC_OPTIONS:
            if demographic_option != selected_demographic:
                options_string = demographic_option.upper() + "_OPTIONS"
                if demographic_option in selected_fields:
                    filters.append(
                        dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                                'name': demographic_option},
                                options=[{'value': o, 'label': o} for o in getattr(
                                    database_constants, options_string)],
                                clearable=True,
                                value=filter_dict[demographic_option],
                                placeholder=demographic_option.replace(
                                    "_", " ").title() + "..."
                                ))
                    )
                else:
                    filters.append(
                    dbc.Col(dcc.Dropdown(id={'type': 'graph_filter',
                                               'name': demographic_option},
                             options=[{'value': o, 'label': o} for o in getattr(
                                 database_constants, options_string)],
                             clearable=True,
                             value='',
                             placeholder=demographic_option.replace(
                                 "_", " ").title() + "..."
                             ))
                    )
        return filters


    @bar_app.callback(
            Output('bar_graph', 'figure'),
            [Input('filter_options', 'children'),
            State('site_options', 'value'),
            State('demographic', 'value'),
            State({'type': 'graph_filter', 'name': dash.ALL}, 'value')]

    )
    def update_bar_graph(html, selected_sites, selected_demographic, selected_filters):
        if selected_sites is None and selected_demographic is None and selected_filters is None:
            raise dash.exceptions.PreventUpdate
        selected_fields = list(dash.callback_context.states.keys())
        selected_fields.pop(0)
        selected_fields.pop(0)
        selected_fields = [eval(field.strip(".value"))
                                for field in selected_fields]
        selected_fields = [field["name"] for field in selected_fields]
        filter_dict = dict(zip(selected_fields, selected_filters))
        selected_fields.append("meal_site")
        selected_fields.append("entry_timestamp")

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
                histogram = px.histogram(combined_df, x=selected_demographic,
                color='meal_site', barmode='group', title=f"Comparison of {selected_demographic} of Diners at Selected Meal Sites")
                return histogram
            else:
                all_site_data = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields)
                all_histogram = px.histogram(all_site_data, x=selected_demographic,
                color='meal_site', barmode='group',
                title = f"{selected_demographic.title()} of Diners at All Meal Sites")
                return all_histogram

        elif selected_filters:
            # print(filter_dict)
            # print(selected_fields)
            if selected_sites:
                site_dfs = []
                for site in selected_sites:
                    site_filter_dict = filter_dict
                    site_filter_dict["meal_site"] = site
                    site_dfs.append(demographic_db.get_patrons(
                        filter_dict=site_filter_dict, select_fields=selected_fields))
                combined_df = pandas.concat(site_dfs).groupby("meal_site")["entry_timestamp"].count()
                combined_df.rename("count", inplace=True)
                bar_graph = px.bar(combined_df, x = combined_df.index,\
                                    y = "count", title = "Comparison of Diners With Selected Filters At Selected Meal Sites", text_auto = True,
                                    color=combined_df.index)
                bar_graph.update_layout(showlegend=False)
                return bar_graph
                
            else:
                all_site_data = demographic_db.get_patrons(
                                filter_dict=filter_dict, select_fields=selected_fields).groupby("meal_site")["entry_timestamp"].count()
                all_site_data.rename("count", inplace=True)
                bar_graph = px.bar(all_site_data, x = all_site_data.index,\
                                    y = "count", title = "Comparison of Diners With Selected Filters Across All Meal Sites", text_auto = True,
                                    color = all_site_data.index)
                bar_graph.update_layout(showlegend=False)
                return bar_graph




            
            



