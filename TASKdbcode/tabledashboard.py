#!/usr/bin/env python

# -----------------------------------------------------------------------
# tabledashboard.py
# Author: Andres Blanco Bonilla
# Dash app for displaying the table on the admin interface
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
from TASKdbcode import demographic_db
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

def init_tabledashboard(server):
    table_app = dash.Dash(
        __name__,
        server=server,
        external_stylesheets=[CUSTOM_BOOTSTRAP],
        url_base_pathname="/tableapp/")

    # icon="material-symbols:download-rounded" style="color: #194f77;"
    total_entries = demographic_db.get_total_entries()
    # Create Layout
    columns = [1,2,3,4,5,6,7,8,9,10]
    # {"name": "meal site", "id": "meal_site", "type": "text"},
    # {"name": "race", "id": "race", "type": "text"},
    # {"name": "language", "id": "language", "type": "text"},
    # {"name": "age range", "id": "age_range", "type": "text"},
    # {"name": "gender", "id": "gender", "type": "text"},
    # {"name": "zip code", "id": "zip_code", "type": "text"},
    # {"name": "homeless", "id": "homeless", "type": "text"},
    # {"name": "veteran", "id": "veteran", "type": "text"},
    # {"name": "disabled", "id": "disabled", "type": "text"},
    # {"name": "guessed", "id": "guessed", "type": "text"}]
    table_app.layout = html.Div([
        dbc.Container([
        dbc.Row([
            dbc.Col(
                html.H3("View Entry Data", style = {'color':'#ffc88f', 'margin-top':'5px', 'margin-left':'5px'}), 
                width = 3, style = {'margin-left':'7px','margin-right':'0px'}),
            dbc.Col(
                html.Div(className="vr", style={"margin-right": "0px",'height':'60px'}), width = 1, align = "center"),
            dbc.Col(
                html.Div(id='num_entries_display', children=[], style = {'color':'white'}), width = 4),
            dbc.Col([
                dbc.Row(dbc.Col(dbc.Button([di(icon = "material-symbols:download-rounded",
                                       id="dlhelp", color = "white", height = 20, style = {'marginRight':'5'}), html.Span("Download"), html.Strong(" Current "), html.Span("Entry Data Excel")],
                                   id="btn_xlsxc", style = {"background-color": "#0085Ca"}))),
                dbc.Row(dbc.Col(dbc.Button([di(icon = "material-symbols:download-rounded",
                                       id="dlchelp", color = "white", height = 20, style = {'marginRight':'5'}), html.Span("Download"), html.Strong(" All "), html.Span("Entry Data Excel")],
                                   id="btn_xlsxa", style = {"background-color": "#0085Ca"})))
        ], style={'margin-bottom':"5px", 'margin-top':'5px', 'margin-left':"5px"}, align = "center")]),

        dcc.Store(id='num_total_entries', data=total_entries),
        dcc.Download(id="download-dataframe-xlsxc"),
        dcc.Download(id="download-dataframe-xlsxa"),
        dbc.Row([
            dash_table.DataTable(
            id='table-filtering',
            columns=[
                {"name": "entry timestamp", "id": "entry_timestamp", "type": "datetime"},
                {"name": "meal site", "id": "meal_site", "type": "text"},
                {"name": "race", "id": "race", "type": "text"},
                {"name": "language", "id": "language", "type": "text"},
                {"name": "age range", "id": "age_range", "type": "text"},
                {"name": "gender", "id": "gender", "type": "text"},
                {"name": "zip code", "id": "zip_code", "type": "text"},
                {"name": "homeless", "id": "homeless", "type": "text"},
                {"name": "veteran", "id": "veteran", "type": "text"},
                {"name": "disabled", "id": "disabled", "type": "text"},
                {"name": "guessed", "id": "guessed", "type": "text"}    
            ],
            css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
            tooltip_header={
                'entry_timestamp': 'Enter a date and/or time in YYYY-MM-DD\'T\'HH:MM:SS format to filter for a specific year, month, date, or time.',
        'meal_site': 'Filter for meal site. Use the \'or\' character with spaces to get more than one meal site',
        'race': 'Enter \'race1\' to filter for all entries containing race1 (including multiracial), and \
        enter \'eq race1\' to filter for entries exactly equal race1. Enter \',\' to filter for all mutliracial entries.\
             Use the \'or\' character with spaces to get more than one race.',
        'language':'Filter for language. Use the \'or\' character with spaces to get more than one language. Type in \'eq \' with a space afterwards\
             before your input to match exactly.',
        'age_range': 'Filter for age range. Use the \'or\' character with spaces to get more than one type. To use this, type in a range such as 18-24, or type \
            >x, >=x, <x, or <=x where x is some number. Just entering a number or a non-predefined range will not work.',
        'gender': 'Filter for gender. Use the \'or\' character with spaces to get more than one type.',
        "zip_code": 'Filter for zip code. Use the \'or\' character with spaces to get more than one type.',
        "homeless": 'Filter for homeless status. Use the \'or\' character with spaces to get more than one type.',
        "veteran": 'Filter for veteran status. Use the \'or\' character with spaces to get more than one type.',
        "disabled": 'Filter for disabled status. Use the \'or\' character with spaces to get more than one type.',
        "guessed": 'Filter for guessed status. Use the \'or\' character with spaces to get more than one type.',
    },
    tooltip_delay=0,
    tooltip_duration=None,
            style_table = {'overflowY': 'auto',
                'height':'80vh', 'width':'100%'
            },
            style_cell={'textAlign': 'left',
                        'height': 'auto'},
            style_cell_conditional=[
                {'if': {'column_id': 'entry_timestamp'},
                 'width': '15%'},
                {'if': {'column_id': 'meal_site'},
                 'width': '13%'},
                {'if': {'column_id': 'race'},
                 'width': '11%'},
                {'if': {'column_id': 'gender'},
                 'width': '9%'}
            ],
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
            # style_as_list_view = True,
            page_current=0,
            page_count = int(math.ceil(total_entries / PAGE_SIZE)),
            page_size=PAGE_SIZE,
            page_action='custom',
            row_deletable=True,
            filter_action='custom',
            filter_query='',
            sort_action='custom',
            sort_mode='multi',
            sort_by=[],
        )
        ], className = "g-0")], fluid = True, style = {'padding':'0px'})], style = {'display':'block', 'background-color': '#145078',
                                                                                    'height': '100vh', 'width': '100%', 'overflow':'scroll'}
        )

    init_callbacks(table_app)
    helpers.protect_dashviews(table_app)

    return table_app.server


def split_filter_part(filter_part):
    # print(filter_part)
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find(
                    '{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    value = value_part

                if " or " in value:
                    value = value.split(" or ")
                else:
                    value = str(value)

                return {"field": name, "op": operator_type[0].strip(),
                        "value": value}

    return {}

# update non time-based filters
# fix age range filter


def init_callbacks(table_app):

    @table_app.callback(
    Output("download-dataframe-xlsxa", "data"),
    [Input("btn_xlsxa", "n_clicks")],
    prevent_initial_call=True)
    def download_all(n_clicks):
        df = demographic_db.get_patrons()
        return dcc.send_data_frame(df.to_excel, "alltaskdata.xlsx", sheet_name="TASK_data_all")

    @table_app.callback(
    Output("download-dataframe-xlsxc", "data"),
    [Input("btn_xlsxc", "n_clicks"),
    State('table-filtering', 'filter_query')],
    prevent_initial_call=True)
    def download_current(n_clicks, filter):
        filtering_expressions = filter.split(' && ')
        filter_dicts = []
        time_filter = {}

        for filter_part in filtering_expressions:

            filter_dict = split_filter_part(filter_part)

            if filter_dict:
                if filter_dict["op"] == "contains":
                    filter_dict["op"] = "ilike"
                    if type(filter_dict["value"]) is list:
                        for index, subvalue in enumerate(filter_dict["value"]):
                            filter_dict["value"][index] = "%" + \
                                subvalue + "%"
                    else:
                        filter_dict["value"] = "%" + \
                                filter_dict["value"] + "%"
                        
                if filter_dict["op"] == "=":
                    filter_dict["op"] = "=="

                if filter_dict["op"] == "datestartswith":
                    time_filter = filter_dict
                else:
                    filter_dicts.append(filter_dict)
        
        df = demographic_db.filter_dms(filter_dicts)
    
        if time_filter:
            df = df.loc[df["entry_timestamp"].astype(str).str.startswith(time_filter["value"])]

        return dcc.send_data_frame(df.to_excel, "taskdatacurrent.xlsx", sheet_name="TASK_data_current")

    @table_app.callback(
        Output('table-filtering', 'data'),
        Output('num_entries_display', 'children'),
        [Input('table-filtering', "page_current"),
        Input('table-filtering', "page_size"),
        Input('table-filtering', 'sort_by'),
        Input('table-filtering', "filter_query")])
    def update_table(page_current, page_size, sort_by, filter):
        # print(filter)
        filtering_expressions = filter.split(' && ')
        filter_dicts = []
        time_filter = {}


        for filter_part in filtering_expressions:

            filter_dict = split_filter_part(filter_part)
            # print(filter_dict)
            

            if filter_dict:
                if filter_dict["op"] == "contains":
                    filter_dict["op"] = "ilike"
                    if type(filter_dict["value"]) is list:
                        for index, subvalue in enumerate(filter_dict["value"]):
                            filter_dict["value"][index] = "%" + \
                                subvalue + "%"
                    else:
                        filter_dict["value"] = "%" + \
                                filter_dict["value"] + "%"
                        
                if filter_dict["op"] == "=":
                    filter_dict["op"] = "=="

                if filter_dict["op"] == "datestartswith":
                    time_filter = filter_dict
                else:
                    filter_dicts.append(filter_dict)

        print(filter_dicts)

        dff = demographic_db.filter_dms(filter_dicts)
        if time_filter:
            dff = dff.loc[dff["entry_timestamp"].astype(str).str.startswith(time_filter["value"])]
            print(dff)

        num_entries = len(dff.index)
        num_total = demographic_db.get_total_entries()
            

        # selected_sites = list(dff["meal_site"].unique())
        # total_site_entries = 0
        # for site in selected_sites:
        #     total_site_entries+=demographic_db.get_num_entries(site)
        # percent_site_data = (num_entries / total_site_entries)

        display = html.H4(["Currently Showing:", html.Br(), f"{num_entries} / {num_total} Entries"], style = {'margin-top': '5px'})
        # display.append(html.H5(f"{num_entries} Entries / {total_site_entries} Total Site Entries = {percent_site_data:.2%} of selected site data"))

        # if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
        #     # these operators match pandas series operator method names
        #     dff = dff.loc[getattr(
        #         dff[col_name], operator)(filter_value)]
        # elif operator == 'contains':
        #     dff = dff.loc[dff[col_name].str.contains(filter_value)]
        # elif operator == 'datestartswith':
        #     # this is a simplification of the front-end filtering logic,
        #     # only works with complete fields in standard format
        #     dff = dff.loc[dff[col_name].str.startswith(
        #         filter_value)]

        if sort_by:
            dff = dff.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )

        return (dff.iloc[
            page_current*page_size:(page_current + 1)*page_size
        ].to_dict('records'), display)
