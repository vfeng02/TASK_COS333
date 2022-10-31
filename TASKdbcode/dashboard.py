#!/usr/bin/env python

#-----------------------------------------------------------------------
# dashboard.py
# Author: Andres Blanco Bonilla
# Test
#-----------------------------------------------------------------------

"""Instantiate a Dash app."""
import dash
from dash import Dash, dash_table
from dash.dependencies import Input, Output
from dash import dcc
from dash import html

import demographic_db

PAGE_SIZE = 50
operators = [['ge ', '>='],
                 ['le ', '<='],
                 ['lt ', '<'],
                 ['gt ', '>'],
                 ['ne ', '!='],
                 ['eq ', '='],
                 ['contains']]


def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/")
    # Load DataFrame
    select_fields = []
    filter_dict = {}
    df = demographic_db.get_patrons(select_fields, filter_dict)

    # Create Layout
    dash_app.layout = dash_table.DataTable(
        id='table-filtering',
        columns=[
            {"name": i, "id": i} for i in df.columns
            
        ],
       # style_as_list_view = True,
        page_current=0,
        page_size=PAGE_SIZE,
        page_action='custom',

        filter_action='custom',
        filter_query=''
    )

    init_callbacks(dash_app)

    return dash_app.server


def split_filter_part(filter_part):
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
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return {"field": name, "op": operator_type[0].strip(),\
                    "value": value}

    return {}

# update non time-based filters
def init_callbacks(dash_app):
    @dash_app.callback(
        Output('table-filtering', "data"),
        Input('table-filtering', "page_current"),
        Input('table-filtering', "page_size"),
        Input('table-filtering', "filter_query"))
    def update_table(page_current, page_size, filter):
        print(filter)
        filtering_expressions = filter.split(' && ')
        dff = None
        for filter_part in filtering_expressions:

            filter_dict = split_filter_part(filter_part)
            print(filter_dict)
            if filter_dict:
                if filter_dict["op"] == "contains":
                    filter_dict["op"] = "ilike"
                    filter_dict["value"] = "%" + filter_dict["value"] + "%"
                if filter_dict["op"] == "=":
                    filter_dict["op"] = "=="

            dff = demographic_db.filter_dm(filter_dict)

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

        return dff.iloc[
            page_current*page_size:(page_current + 1)*page_size
        ].to_dict('records')


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id="database-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=300,
    )
    return table
