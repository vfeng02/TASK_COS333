#!/usr/bin/env python

# -----------------------------------------------------------------------
# graphdashboard.py
# Author: Andres Blanco Bonilla
# Test
# -----------------------------------------------------------------------

"""Instantiate a Dash app."""
import dash
import pandas
from TASKdbcode import demographic_db
from TASKdbcode import database_constants
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def init_graphdashboard(server):
    graph_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/graphapp/")
    
    df = demographic_db.get_patrons([], {})
    demographic_options = []
    for option in database_constants.DEMOGRAPHIC_OPTIONS:
        demographic_options.append({"label": option.title(), "value": option})
# additional filtering needed
    graph_app.layout = html.Div(
        children=[
            html.Div(children=[
                dcc.Dropdown(id='dropdown1',
                             options=[{'value': x, 'label': x}
                                      for x in df.meal_site.unique()],
                             clearable=False,
                             value='First Baptist Church',
                             ),
                dcc.Dropdown(id='dropdown2',
                             options=demographic_options,
                             clearable=False,
                             value='race',
                             )
            ], className='menu-l'
            ),
            dcc.Graph(id='interaction2',
                      config={'displayModeBar': False},
                      className='card',
                      style={'width': '100vw', 'height': '100vh'})
        ]
    )
    
    init_callbacks(graph_app)

    return graph_app.server

def init_callbacks(graph_app):
    
    @graph_app.callback(
            Output('interaction2', 'figure'),
            [Input('dropdown1', 'value'),
                Input('dropdown2', 'value')]
        # B) defining the callback and what to return here
    )
    def update_pie_chart(select_d1,select_d2):
        site_df = demographic_db.get_patrons([], {"meal_site": select_d1})
        if select_d2 == "race":
            all_counts = site_df["race"].value_counts()
            single_index = [i for i in all_counts.index if i in database_constants.RACE_OPTIONS]
            multi_index = [i for i in all_counts.index if i not in database_constants.RACE_OPTIONS]
            single_counts = all_counts.filter(items = single_index)
            multi_counts = all_counts.filter(items = multi_index)
            num_multi = multi_counts.size
            multi_count = pandas.Series([num_multi], ["Other/Multiracial"])
            summary_counts = pandas.concat([single_counts, multi_count])
            # print(summary_counts)
            specs = [[{'type':'domain'}], [{'type':'domain'}]]
            pie_charts = make_subplots(rows=2, cols=1, specs=specs)
            single_chart = go.Pie(values = summary_counts, labels = summary_counts.index,
                                  title = f"Races of Single Race Patrons at {select_d1} Meal Site",
                                  legendgroup=1)
            other_chart = go.Pie(values = multi_counts, labels = multi_counts.index,
                            title = f"Other: Races of Multi-Racial Patrons at {select_d1} Meal Site", legendgroup=2)
            pie_charts.add_trace(single_chart, 1, 1)
            pie_charts.add_trace(other_chart, 2, 1)
            # This is how many pixels apart to put the 2 charts
            pie_charts.update_layout(legend_tracegroupgap = 120)
            pie_charts.update_layout(title=f"Races of Patrons at {select_d1} Meal Site")
            return pie_charts
        else:
            ## using dash to make the pie chart
            pie_chart=go.Figure(data=[go.Pie(labels=site_df[select_d2].value_counts().index.tolist(),
                                        values=list(site_df[select_d2].value_counts()))])
            
            ## customizing the title of the pie chart
            pie_chart.update_layout(title=
            f"{select_d2.title()} of Patrons at {select_d1}"
                        " Meal Site")
            return pie_chart

            
            



