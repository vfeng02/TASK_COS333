#!/usr/bin/env python

#-----------------------------------------------------------------------
# graphdashboard.py
# Author: Andres Blanco Bonilla
# Test, obsolete now
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


def init_graphdashboard(server):
    graph_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/graphapp/",
        external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    df = demographic_db.get_patrons()
    demographic_options = []
    for option in database_constants.DEMOGRAPHIC_OPTIONS:
        demographic_options.append({"label": option.title(), "value": option})

# added dropdowns for filtering
# the dropdowns are on a bootstrap grid made using dash bootstrap components (dbc)
    graph_app.layout = html.Div(
        children=[
            html.Div(children=[
                html.H4("Select a Meal Site and a Demographic"),
                dcc.Dropdown(id='site',
                             options=[{'value': x, 'label': x}
                                      for x in df.meal_site.unique()],
                             clearable=False,
                             value='First Baptist Church'
                             ),
                dcc.Dropdown(id='demographic',
                             options=demographic_options,
                             clearable=False,
                             value='race'
                             )
                , html.H4("Select Filters"),
                dbc.Row(id = "filter_options", children = [])
            ], className='menu-l'
            ),
            dcc.Graph(id='interaction2',
                      config={'displayModeBar': True, 'displayLogo': False},
                      className='card',
                      style = {'width': '100vw', 'height': '100vh'}
                      )
        ]
    )
    
    init_callbacks(graph_app)

    return graph_app.server

def init_callbacks(graph_app):
    
    
    # this callback is called when a demographic is selected
    # it removes that demographic from the filter dropdown options
    # bc that would make no sense
    @graph_app.callback(
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
    
    # this calllback is called whenever the site, demographic, or any of the filter drop downs change
    # and creates a new graph based on that
    @graph_app.callback(
            Output('interaction2', 'figure'),
            [Input('site', 'value'),
            Input('demographic', 'value'),
            Input({'type': 'graph_filter', 'name': dash.ALL}, 'value')]
    )
    def update_pie_chart(selected_site, selected_demographic, selected_filters):
        selected_fields = list(dash.callback_context.inputs.keys())
        selected_fields.pop(0)
        selected_fields.pop(0)
        selected_fields = [eval(field.strip(".value")) for field in selected_fields]
        selected_fields = [field["name"] for field in selected_fields]
        filter_dict = dict(zip(selected_fields, selected_filters))
        selected_fields.append(selected_demographic)
            
        site_df = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields)
        #print(site_df)
        if selected_demographic == "race":
            all_counts = site_df["race"].value_counts()
            single_index = [i for i in all_counts.index if i in database_constants.RACE_OPTIONS]
            multi_index = [i for i in all_counts.index if i not in database_constants.RACE_OPTIONS]
            single_counts = all_counts.filter(items = single_index)
            multi_counts = all_counts.filter(items = multi_index)
            num_multi = multi_counts.size
            multi_count = pandas.Series([num_multi], ["Other/Multi-Racial"])
            summary_counts = pandas.concat([single_counts, multi_count])
            # print(summary_counts)
            specs = [[{'type':'domain'}], [{'type':'domain'}]]
            pie_charts = make_subplots(rows=2, cols=1, specs=specs)
            # the titles of the charts could posssibly include the filters but idk how to make that look good
            single_chart = go.Pie(values = summary_counts, labels = summary_counts.index,
                                  title = f"Races of Single Race Diners at {selected_site} Meal Site",
                                  legendgroup=1)
            other_chart = go.Pie(values = multi_counts, labels = multi_counts.index,
                            title = f"Other/Multiracial: Races of Multi-Racial Diners at {selected_site} Meal Site", legendgroup=2)
            pie_charts.add_trace(single_chart, 1, 1)
            pie_charts.add_trace(other_chart, 2, 1)
            # This is how many pixels apart to put the 2 charts
            # maybe experiment with putting them side by side? idk how it works
            pie_charts.update_layout(legend_tracegroupgap = 110)
            pie_charts.update_layout(title=f"Races of Diners at {selected_site} Meal Site")
            return pie_charts
        else:
            ## using dash to make the pie chart
            pie_chart=go.Figure(data=[go.Pie(labels=site_df[selected_demographic].value_counts().index.tolist(),
                                        values=list(site_df[selected_demographic].value_counts()))])
            
            ## customizing the title of the pie chart
            # titles could be different to include active filters
            # also stuff like "Homeless of Diners at Meal Site" makes no sense lol that needs to be different
            pie_chart.update_layout(title=
            f"{selected_demographic.title()} of Diners at {selected_site}"
                        " Meal Site")
            return pie_chart

            
            



