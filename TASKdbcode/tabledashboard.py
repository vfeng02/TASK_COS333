#!/usr/bin/env python

# -----------------------------------------------------------------------
# tabledashboard.py
# Author: Andres Blanco Bonilla
# Dash app for displaying the table on the admin interface
# -----------------------------------------------------------------------

"""Instantiate a Dash app."""
import dash
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
import pandas
from TASKdbcode import demographic_db

PAGE_SIZE = 100
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains']]

def init_tabledashboard(server):
    table_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/tableapp/")
    # Load DataFrame
    df = demographic_db.get_patrons()

    # Create Layout
    table_app.layout = html.Div([
        dcc.Store(id='num_total_entries', data=len(df.index)),
        html.Div(id='num_entries_display', style={
                 'font-family': 'Courier New'}, children=[]),
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
            style_cell={'textAlign': 'left',
                        'height': 'auto'},
            style_cell_conditional=[
                {'if': {'column_id': 'entry_timestamp'},
                 'width': '17%'},
                {'if': {'column_id': 'meal_site'},
                 'width': '15%'},
                {'if': {'column_id': 'race'},
                 'width': '15%'},
                {'if': {'column_id': 'gender'},
                 'width': '7%'}
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
            page_size=PAGE_SIZE,
            page_action='custom',

            filter_action='custom',
            filter_query='',

            sort_action='custom',
            sort_mode='multi',
            sort_by=[],
        )
    ])

    init_callbacks(table_app)

    return table_app.server


def split_filter_part(filter_part):
    print(filter_part)
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
                    try:
                        value = int(value_part)
                    except ValueError:
                        value = value_part

                if " or " in value:
                    value = value.split(" or ")

                return {"field": name, "op": operator_type[0].strip(),
                        "value": value}

    return {}

# update non time-based filters
# fix age range filter


def init_callbacks(table_app):

    @table_app.callback(
        Output('table-filtering', 'data'),
        Output('num_entries_display', 'children'),
        Input('table-filtering', "page_current"),
        Input('table-filtering', "page_size"),
        Input('table-filtering', 'sort_by'),
        Input('table-filtering', "filter_query"))
    def update_table(page_current, page_size, sort_by, filter):
        # print(filter)
        filtering_expressions = filter.split(' && ')
        filter_dicts = []

        for filter_part in filtering_expressions:

            filter_dict = split_filter_part(filter_part)
            print(filter_dict)

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
                filter_dicts.append(filter_dict)

        dff = demographic_db.filter_dms(filter_dicts)
        num_entries = len(dff.index)

        # selected_sites = list(dff["meal_site"].unique())
        # total_site_entries = 0
        # for site in selected_sites:
        #     total_site_entries+=demographic_db.get_num_entries(site)
        # percent_site_data = (num_entries / total_site_entries)

        display = [
            html.H4(f"Number of Entries Currently in Table: {num_entries}")]
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
