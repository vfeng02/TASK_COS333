#!/usr/bin/env python

#-----------------------------------------------------------------------
# dashboard.py
# Author: Andres Blanco Bonilla
# Test
#-----------------------------------------------------------------------

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


def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/")
    # Load DataFrame
    select_fields = []
    filter_dict = {}
    df = demographic_db.get_patrons(select_fields, filter_dict)

    # Create Layout
    dash_app.layout = html.Div([
        dcc.Store(id='table'),
        dcc.Store(id='filters'),
        dash_table.DataTable(
        id='table-filtering',
        columns=[
            {"name": i, "id": i} for i in df.columns
            
        ],
        style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data={
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
        'fontWeight': 'bold'
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
                        value = int(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return {"field": name, "op": operator_type[0].strip(),\
                    "value": str(value)}

    return {}

# update non time-based filters
# fix age range filter

def init_callbacks(dash_app):
    
    # @dash_app.callback(
    #     Output('table', 'data'),
    #     Input('table-filtering', 'filter_query'),
    #     Input('filters', 'data'))
    # def filter_data(new_filters, old_filters):
    #  # some expensive data processing step
    #  old_filters = pandas.read_json(old_filters, orient='split')
    #  filtering_expressions = new_filters.split(' && ')
     
    #  dff = pandas.read_json(jsonified_cleaned_data, orient='split')
     
    #  cleaned_df = slow_processing_step(value)


    #  # more generally, this line would be
    #  # json.dumps(cleaned_df)
    #  return cleaned_df.to_json(date_format='iso', orient='split')
 
    @dash_app.callback(
        Output('table-filtering', "data"),
        Input('table-filtering', "page_current"),
        Input('table-filtering', "page_size"),
        Input('table-filtering', 'sort_by'),
        Input('table-filtering', "filter_query"))
    def update_table(page_current, page_size, sort_by, filter):
        print(filter)
        filtering_expressions = filter.split(' && ')
        filter_dicts = []
        
        for filter_part in filtering_expressions:

            filter_dict = split_filter_part(filter_part)
            print(filter_dict)

            if filter_dict:
                if filter_dict["op"] == "contains":
                    filter_dict["op"] = "ilike"
                    filter_dict["value"] = "%" + filter_dict["value"] + "%"
                if filter_dict["op"] == "=":
                    filter_dict["op"] = "=="
                filter_dicts.append(filter_dict)

        dff = demographic_db.filter_dms(filter_dicts)
                

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

        return dff.iloc[
            page_current*page_size:(page_current + 1)*page_size
        ].to_dict('records')


