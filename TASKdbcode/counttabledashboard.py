#!/usr/bin/env python

# -----------------------------------------------------------------------
# counttabledashboard.py
# Author: Andres Blanco Bonilla
# Dash app for displaying the "View Count Data" tab (counttable)
# on the admin interface.
# route: /counttableapp
# -----------------------------------------------------------------------

"""Instantiate a Dash app."""
import math
import dash
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify as di
import pandas
import xlsxwriter
from functools import reduce
from TASKdbcode import demographic_db
from TASKdbcode import database_constants
from TASKdbcode import graphdashboard_helpers as helpers

PAGE_SIZE = 100
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains'],
             ['datestartswith']]

CUSTOM_BOOTSTRAP = '../static/custombootstrap.min.css'

def init_counttabledashboard(server):
    count_table_app = dash.Dash(
        __name__,
        server=server,
        external_stylesheets=[CUSTOM_BOOTSTRAP],
        url_base_pathname="/counttableapp/")


    # failed attempt at creating table
    # dff = demographic_db.get_patrons()
    # count_df_list = []
    # for option in database_constants.DEMOGRAPHIC_OPTIONS:
    #     count_df = dff.groupby(['meal_site', option]).size().unstack(fill_value=0)
    #     if option in list(database_constants.STATUS_OPTION_MAPPING):
    #         print(database_constants.STATUS_OPTION_MAPPING[option])
    #         count_df.rename(columns = database_constants.STATUS_OPTION_MAPPING[option], inplace = True)
    #             #print(count_df)
    #         count_df_list.append(count_df)
        
    # counts_df = reduce(lambda df1,df2: pandas.merge(df1,df2,on='meal_site'), count_df_list)
    
    count_table_app.layout = html.Div([
        dbc.Container([
        dbc.Row([
            dbc.Col(
                html.H3("View Count Data", style = {'color':'#ffc88f', 'margin-top':'5px', 'margin-left':'5px'}), 
                width = 3, style = {'margin-left':'7px','margin-right':'0px'}),
            dbc.Col(
                html.Div(className="vr", style={"margin-right": "0px", 'padding-right': '0px', 'height':'10vh'}), width = 1, align = "center"),
            dbc.Col([
                html.Div([
                    html.H4("Select Demographic Categories for Counts", style={
                            'display': 'inline-block', 'margin-right': '5px'}),
                    di(icon="material-symbols:help-outline-rounded",
                       id="fhelp", color="white", inline=True, height=20),
                    dbc.Tooltip([html.P("The table will show the counts of the different options for each of the categories you select, at each meal site. Clear your selection to automatically select all categories.",
                                        style={"textAlign": "left", "marginBottom": 0})], target="fhelp", style={"width": 600}),
                ], style={'color': 'white'}),
                html.H5("Show me the counts of...",style={'color': 'white'}),
                dbc.Row(dcc.Dropdown(id='demographic_count_options',
                             options=[{'label': l, 'value': v}
                                      for v, l in database_constants.DEMOGRAPHIC_CATEGORIES.items()],
                             clearable=True,
                             multi=True,
                             placeholder="All Categories"
                             ))
        ], width = 5, style = {'margin-top':'5px', 'margin-bottom':'5px'}, className = "gx-0"),
            dbc.Col([
                dbc.Row(dbc.Col(dbc.Button([di(icon = "material-symbols:download-rounded",
                                       id="dlhelp", color = "white", height = 20, style = {'marginRight':'5'}), html.Span("Download"), html.Strong(" Current "), html.Br(), html.Span("Count Data Excel")],
                                   id="btn_xlsxcc", style = {"background-color": "#0085Ca"}))),
                dbc.Row(dbc.Col(dbc.Button([di(icon = "material-symbols:download-rounded",
                                       id="dlchelp", color = "white", height = 20, style = {'marginRight':'5'}), html.Span("Download"), html.Strong(" All "), html.Span("Count Data Excel")],
                                   id="btn_xlsxac", style = {"background-color": "#0085Ca"})))
        ], style={'margin-bottom':"5px", 'margin-top':'5px', 'margin-left':"5px"}, align = "center")]),
        dcc.Download(id="download-dataframe-xlsxcc"),
        dcc.Download(id="download-dataframe-xlsxac"),
        dbc.Row([
            dash_table.DataTable(
            data = None,
            id='count-table',
            style_table = {'overflowY': 'scroll','overflowX': 'scroll',
                'height':'80vh', 'minWidth':'100%'
            },
            style_cell={'textAlign': 'left',
                        'height': 'auto'},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'color': 'black',
                'backgroundColor': 'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black',
                'fontWeight': 'bold',
            },
            fixed_columns={'headers': True, 'data': 1},
            # style_as_list_view = True,

            sort_action='native',
            sort_mode='multi',
            sort_by=[],
        )
        ], className = "g-0")], fluid = True, style = {'padding':'0px'})], style = {'display':'block', 'background-color': '#145078',
                                                                                    'height': '100vh', 'width': '100%', 'overflow':'scroll'}
        )

    init_callbacks(count_table_app)
    helpers.protect_dashviews(count_table_app)

    return count_table_app.server



def init_callbacks(count_table_app):

    @count_table_app.callback(
    Output("download-dataframe-xlsxac", "data"),
    [Input("btn_xlsxac", "n_clicks")],
    prevent_initial_call=True)
    def download_all(n_clicks):
        count_df_list = []
        df = demographic_db.get_patrons()
        for option in database_constants.DEMOGRAPHIC_OPTIONS:
            count_df = df.groupby(['meal_site', option]).size().unstack(fill_value=0)
            if option in list(database_constants.STATUS_OPTION_MAPPING):
                count_df.rename(columns = database_constants.STATUS_OPTION_MAPPING[option], inplace = True)
                #print(count_df)
            else:
                count_df.rename(columns = {"Unknown":f"Unknown {option.title()}", "Other":f"Other {option.title()}"}, inplace=True)
            count_df_list.append(count_df)
        
        counts_df = reduce(lambda df1,df2: pandas.merge(df1,df2,on='meal_site'), count_df_list)
        counts_df.reset_index(inplace=True)
        counts_df.rename(columns = {'meal_site':'meal site'}, inplace=True)
        return dcc.send_data_frame(counts_df.to_excel, "alltaskcountdata.xlsx", sheet_name="TASK_count_data_all")

    @count_table_app.callback(
    Output("download-dataframe-xlsxcc", "data"),
    [Input("btn_xlsxcc", "n_clicks"),
    State('demographic_count_options', 'value')],
    prevent_initial_call=True)
    def download_current(n_clicks, selected_categories):
        if selected_categories:
            category_list = selected_categories
            selected_fields = ["meal_site", *category_list]
        else:
            selected_fields = []
            category_list = database_constants.DEMOGRAPHIC_OPTIONS

        df = demographic_db.get_patrons(select_fields=selected_categories)

        count_df_list = []
        for option in category_list:
            count_df = df.groupby(['meal_site', option]).size().unstack(fill_value=0)
            if option in list(database_constants.STATUS_OPTION_MAPPING):
                print(database_constants.STATUS_OPTION_MAPPING[option])
                count_df.rename(columns = database_constants.STATUS_OPTION_MAPPING[option], inplace = True)
                #print(count_df)
            else:
                count_df.rename(columns = {"Unknown":f"Unknown {option.title()}", "Other":f"Other {option.title()}"}, inplace=True)

            count_df_list.append(count_df)
        
        counts_df = reduce(lambda df1,df2: pandas.merge(df1,df2,on='meal_site'), count_df_list)
        counts_df.reset_index(inplace=True)
        counts_df.rename(columns = {'meal_site':'meal site'}, inplace=True)
        
        return dcc.send_data_frame(df.to_excel, "taskcountdatacurrent.xlsx", sheet_name="TASK_count_data_current")

    # This callback updates the count table display with the data
    # that matches the currently selected demographic categories.
    @count_table_app.callback(
        Output('count-table', 'data'),
        Input('demographic_count_options', 'value'))
    def update_table(selected_categories):
        
        if selected_categories:
            category_list = selected_categories
            selected_fields = ["meal_site", *category_list]
        else:
            selected_fields = []
            category_list = database_constants.DEMOGRAPHIC_OPTIONS

        df = demographic_db.get_patrons(select_fields=selected_fields)
        
        count_df_list = []

        for option in category_list:
            count_df = df.groupby(['meal_site', option]).size().unstack(fill_value=0)
            if option in list(database_constants.STATUS_OPTION_MAPPING):
                print(database_constants.STATUS_OPTION_MAPPING[option])
                count_df.rename(columns = database_constants.STATUS_OPTION_MAPPING[option], inplace = True)
            else:
                count_df.rename(columns = {"Unknown":f"Unknown {option.title()}", "Other":f"Other {option.title()}"}, inplace=True)
            count_df_list.append(count_df)
        
        counts_df = reduce(lambda df1,df2: pandas.merge(df1,df2,on='meal_site'), count_df_list)
        counts_df.reset_index(inplace=True)
        counts_df.rename(columns = {'meal_site':'meal site'}, inplace=True)
        # Testing a display that I ended up thinking was ugly
        # display = html.H4(["Currently Showing: All Count Data", html.Br()], style = {'margin-top': '5px'})
        # display.append(html.H5(f"{num_entries} Entries / {total_site_entries} Total Site Entries = {percent_site_data:.2%} of selected site data"))
        # if len(filter_text_list) > 1:
        #     filter_string = ', '.join(
        #         filter_text_list[:-1]) + ', and ' + filter_text_list[-1] + " "
        # elif len(filter_text_list) == 1:
        #     filter_string = filter_text_list[0] + " "
        # else:
        #     filter_string = ""
        return (counts_df.to_dict('records'))
