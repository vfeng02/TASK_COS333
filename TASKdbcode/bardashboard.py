#!/usr/bin/env python

#-----------------------------------------------------------------------
# bardashboard.py
# Author: Andres Blanco Bonilla
# Dash app for bar graph display
# route: /barapp
#-----------------------------------------------------------------------

"""Instantiate a Dash app."""
import datetime
import dash
import pandas
from TASKdbcode import demographic_db
from TASKdbcode import database_constants
from TASKdbcode import graphdashboard_helpers as helpers
from dash import dcc
from dash import html
from dash_iconify import DashIconify as di
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

CUSTOM_BOOTSTRAP = 'assets/bootstrap.min.css'

def init_bardashboard(server):
    bar_app = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix="/barapp/",
        # using the default bootstrap style sheet, could be changed
        external_stylesheets=[CUSTOM_BOOTSTRAP])

    bar_app.layout = html.Div(
        children=[
            dbc.Container([
            dbc.Row([
            dbc.Col([
            html.H3("Graph by Meal Site", style = {'color':'#ffc88f', 'margin-top':'5px', 'font-weight':'bold'}),
            html.Div([
                html.Div([
                    html.Hr(style={"width": "100%", 'borderTop': '3px solid #ff911f','borderBottom': '2px #ff911f',"opacity": "unset"}),
                    html.H4("Select Meal Sites", style={
                            'display': 'inline-block', 'margin-right': '5px','color': 'white'}),
                    di(icon="material-symbols:help-outline-rounded",
                       id="mshelp", color="white", inline=True, height=20),
                    dbc.Tooltip([html.P("Select the meal sites whose entries you want to be included in the bar graph. Each meal site will get its own bar, or set of bars, on the graph. Clear your selection to automatically select any/all meal sites.",
                                        style={"textAlign": "left", "marginBottom": 0})], target="mshelp", style={"width": 600}),
                    html.H5("Compare data from diners at...", style = {"color":"white"})]),
                dcc.Dropdown(id='site_options',
                             options=[{'value': o, 'label': o}
                                      for o in database_constants.MEAL_SITE_OPTIONS],
                             clearable=True,
                             multi=True,
                             value=["Trenton Area Soup Kitchen"],
                             placeholder="All Meal Sites"
                             ),
                html.Hr(style={"width": "100%", 'borderTop': '3px solid #ff911f','borderBottom': '2px #ff911f',"opacity": "unset"}),
                html.Div([
                    html.H4("Select Filters on Diners", style={
                            'display': 'inline-block', 'margin-right': '5px'}),
                    di(icon="material-symbols:help-outline-rounded",
                       id="fhelp", color="white", inline=True, height=20),
                    dbc.Tooltip([html.P("The bar graph will only include data from diners who meet the criteria of all your selected filters. Clear a filter selection to automatically include any/all options of that category.",
                                        style={"textAlign": "left", "marginBottom": 0})], target="fhelp", style={"width": 600}),
                ], style={'color': 'white'}),
                html.H5("Make a graph of diners who are...",style={'color': 'white'}),
                dbc.Row(id="filter_options", children=helpers.filter_options_helper(None, {}, "bar")),
                html.Hr(style={"width": "100%", 'borderTop': '3px solid #ff911f','borderBottom': '2px #ff911f',"opacity": "unset"}),
                html.Div([
                    html.H4("Select Category for Bar Grouping", style={
                            'display': 'inline-block', 'margin-right': '5px', 'color': 'white'}),
                    di(icon="material-symbols:help-outline-rounded",
                       id="dchelp", color="white", inline=True, height=20),
                    dbc.Tooltip([html.P("Break down diner data by the category you select. For example, selecting Veteran Status will create slices for Veteran, Not a Veteran, and Unknown on the bar graph.",
                                        style={"textAlign": "left", "marginBottom": 0})], target="dchelp", style={"width": 600}),
                    html.H5("Break down diners by...",style={'color': 'white'})]),
                    dbc.DropdownMenu(
                                [
                                    dbc.DropdownMenuItem(
                                        "Race", id="mrace"),
                                    dbc.DropdownMenuItem(
                                        "Language", id="mlanguage"),
                                    dbc.DropdownMenuItem(
                                        "Age Range", id="mage_range"),
                                    dbc.DropdownMenuItem(
                                        "Gender", id="mgender"),
                                    dbc.DropdownMenuItem(
                                        "Zip Code", id="mzip_code"),
                                    dbc.DropdownMenuItem(divider=True),
                                    dbc.DropdownMenuItem(
                                        "Homeless Status", id="mhomeless"),
                                    dbc.DropdownMenuItem(
                                        "Veteran Status", id="mveteran"),
                                    dbc.DropdownMenuItem(
                                        "Disabled Status", id="mdisabled"),
                                    dbc.DropdownMenuItem(
                                        "Guessed Entry Status", id="mguessed"),
                                    dbc.DropdownMenuItem(divider=True),
                                    dbc.DropdownMenuItem(
                                        "None", id="mnone"),
                                ],
                                label="None",
                                className="mb-3",
                                id='iddropdownmenu',
                                direction="up",
                                color="#0085Ca"
                            ),
                html.Hr(style={"width": "100%", 'borderTop': '3px solid #ff911f','borderBottom': '2px #ff911f',"opacity": "unset"}),

            ], className='menu-l'
            )], width = 4),
            dbc.Col([
            dcc.Graph(id='bar_graph',
                      className = 'card',
                      config={'displayModeBar': True,
                              'displaylogo': False},
                      style={'width': '100%', 'height': '100%',
                             'display':'block'},
                      responsive = True
                      )], width = 8),
        ])], fluid = True)],style = {'display':'block', 'background-color': '#145078',
                                          'min-height':'100%', 'height': '100vh', 'width': '100%', 'overflow':'scroll'}
    )



    init_callbacks(bar_app)

    return bar_app.server


def init_callbacks(bar_app):

    @bar_app.callback(
       Output('filter_options', 'children'),
        Output('iddropdownmenu', 'label'),
        [Input("mrace", "n_clicks"),
         Input("mlanguage", "n_clicks"),
         Input("mage_range", "n_clicks"),
         Input("mgender", "n_clicks"),
         Input("mzip_code", "n_clicks"),
         Input("mhomeless", "n_clicks"),
         Input("mveteran", "n_clicks"),
         Input("mdisabled", "n_clicks"),
         Input("mguessed", "n_clicks"),
         Input("mnone", "n_clicks")],
         [State('range', 'start_date'),
         State('range', 'end_date'),
         State({'type': 'graph_filter', 'name': dash.ALL}, 'value')]
    )
    def update_filter_options(r, l, a, gr, z, h, v, d, gs, n, time_range_start, time_range_end, selected_filters):

        ctx = dash.callback_context
        # print(selected_filters)
        # print(buttons)
        # print(buttons[0])

        if not ctx.triggered:
            button_label = "None"
            selected_demographic = ""
        else:
            button_label = ctx.triggered[0]["prop_id"].split(".")[0]
            selected_demographic = button_label.strip("m")

        if selected_demographic == "none":
            selected_demographic = ""
            button_label = "None"

        selected_fields = helpers.selected_fields_helper(
            dash.callback_context.states)
        filter_dict = dict(zip(selected_fields, selected_filters))
        time_filter = {}
        if time_range_start:
            time_filter["start_date"] = time_range_start
        else:
            time_filter["start_date"] = None
            

        if time_range_end:
            time_filter["end_date"] = time_range_end
        else:
            time_filter["end_date"] = None

        filter_dict["entry_timestamp"] = time_filter
        filters = helpers.filter_options_helper(
            selected_demographic, filter_dict, "pie")

        if selected_demographic:
            button_label = database_constants.DEMOGRAPHIC_CATEGORIES[selected_demographic]
        # print("\n" + button_label + "\n")

        return filters, button_label


    @bar_app.callback(
        Output('bar_graph', 'figure'),
        [Input('site_options', 'value'),
         Input("mrace", "n_clicks"),
         Input("mlanguage", "n_clicks"),
         Input("mage_range", "n_clicks"),
         Input("mgender", "n_clicks"),
         Input("mzip_code", "n_clicks"),
         Input("mhomeless", "n_clicks"),
         Input("mveteran", "n_clicks"),
         Input("mdisabled", "n_clicks"),
         Input("mguessed", "n_clicks"),
         Input("mnone", "n_clicks"),
         Input('range', 'start_date'),
         Input('range', 'end_date')],
         Input({'type': 'graph_filter', 'name': dash.ALL}, 'value'),
        State('iddropdownmenu', 'label')
    )

    def update_bar_graph(selected_sites, r, l, a, gr, z, h, v, d, gs, n, time_range_start, time_range_end, selected_filters, mlabel):

        if dash.callback_context.triggered_id in ("mrace", "mlanguage", "mage_range", "mgender",
                                                  "mzip_code", "mhomeless", "mveteran", "mdisabled",
                                                  "mguessed", "mnone"):
            button_id = dash.callback_context.triggered_id
        elif mlabel == "None":
            button_id = "none"
        else:
            button_id = database_constants.DEMOGRAPHIC_CATEGORIES_SWAPPED[mlabel]

        # print("\n")
        # print(button_id)
        # print("\n")

        if button_id == "mnone" or button_id == "none":
            selected_demographic = ""
        else:
            selected_demographic = button_id.strip("m")

        
        selected_fields = helpers.selected_fields_helper(dash.callback_context.inputs)
        filter_dict = dict(zip(selected_fields, selected_filters))
        selected_fields.append("entry_timestamp")
        selected_fields.append("meal_site")

        time_filter = {}
        if time_range_start:
            time_filter["start_date"] = time_range_start
        else:
            time_filter["start_date"] = datetime.date(2022, 10, 1)

        if time_range_end:
            time_filter["end_date"] = time_range_end
        else:
            time_filter["end_date"] = datetime.date.max

        if time_range_start or time_range_end:
            filter_dict["entry_timestamp"] = time_filter

        # to do for bar graphs:
        # colors repeat sometimes and it may be hard to read, need to change colors
        # but still not great, some sort of "Not Found" message might be good
        if selected_demographic:
            
            selected_fields.append(selected_demographic)
                        
            if selected_sites:
                filter_dict["meal_site"] = selected_sites
#-----------------------------------------------------------------------
            if selected_demographic == "race":
                bar_graph = go.Figure()

                diner_data_df = demographic_db.get_patrons(
                    filter_dict=filter_dict, select_fields=selected_fields)


                if len(diner_data_df.index) == 0:
                    none_found_message = helpers.graph_message("No entries found.")
                    return none_found_message

                if time_range_start and not time_range_end:
                    filter_dict['entry_timestamp']['end_date'] = diner_data_df['entry_timestamp'].head(1).item().date()

                bar_graph_title = helpers.construct_title(
                    filter_dict, graph_type="bar", selected_demographic=selected_demographic)

                diner_data_df.replace(to_replace='American Indian/Alaska Native', value='AI/AN', regex=True, inplace = True)
                diner_data_df.replace(to_replace='Native Hawaiian/Pacific Islander', value='NHOPI', regex=True, inplace = True)
                
                diff_races = list(diner_data_df["race"].unique())
                multi_races = [race for race in diff_races if "," in race]
                multi_races.sort()

                histogram = px.histogram(diner_data_df, x=selected_demographic,
                color='meal_site', barmode='group', text_auto=True)
                histogram.update_layout(yaxis_title = "number of entries")
                histogram.update_xaxes(categoryorder="array", categoryarray = ["White", "Black", "Hispanic", "Asian", "AI/AN", "NHOPI", "Unknown", *multi_races])
                show_sep = []
                # print(histogram.data)
                for trace in histogram.data:
                    trace.visible = False
                    bar_graph.add_trace(trace)
                    show_sep.append(True)
                # return histogram
                
                diner_data_df.loc[diner_data_df["race"].str.contains(","), "race"] = "Multiracial"
                
                g_histogram = px.histogram(diner_data_df, x=selected_demographic,
                color='meal_site', barmode='group', text_auto=True)
                g_histogram.update_layout(yaxis_title = "number of entries")
                g_histogram.update_xaxes(categoryorder="array", categoryarray = ["White", "Black", "Hispanic", "Asian", "AI/AN", "NHOPI", "Unknown", "Multiracial"])
                show_group = []
                for trace in list(g_histogram.data):
                    trace.visible = True
                    bar_graph.add_trace(trace)
                    show_group.append(True)
                bar_graph.update_xaxes(categoryorder = 'array',categoryarray = ["White", "Black", "Hispanic", "Asian", "AI/AN", "NHOPI", "Unknown"])

                bar_graph.update_layout(
                    updatemenus=[
                        dict(
                            type="dropdown",
                            direction="down",
                            active=0,
                            showactive = True,
                            x = 0.60,
                            y = .99,
                            xanchor="left",
                            yanchor="top",
                            buttons=list([
                                dict(label="Group Multiracial",
                                     method="restyle",
                                     args=[{"visible":[not b for b in show_sep] + show_group},]),
                                dict(label="Split Multiracial",
                                     method="restyle",
                                     args=[{"visible": show_sep + [not b for b in show_group]},]),
                            ]),
                        )
                    ],
                    title = bar_graph_title,
                    yaxis_title = "number of entries",
                    xaxis_title = "race")
                
                return bar_graph
#-----------------------------------------------------------------------
    
            diner_data_df = demographic_db.get_patrons(
                        filter_dict=filter_dict, select_fields=selected_fields)

            if len(diner_data_df.index) == 0:
                    none_found_message = helpers.graph_message("No entries found.")
                    return none_found_message

            if time_range_start and not time_range_end:
                filter_dict['entry_timestamp']['end_date'] = diner_data_df['entry_timestamp'].head(1).item().date()

            histogram_title = helpers.construct_title(filter_dict, graph_type="bar", selected_demographic=selected_demographic)
            histogram = px.histogram(diner_data_df, x=selected_demographic,
            color='meal_site', barmode='group', title=histogram_title, text_auto=True)
            histogram.update_layout(yaxis_title = "number of entries")
            return histogram

        else:

            if selected_sites:
                filter_dict["meal_site"] = selected_sites
                
            diner_data = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields)

            if len(diner_data.index) == 0:
                    none_found_message = helpers.graph_message("No entries found.")
                    return none_found_message

            if time_range_start and not time_range_end:
                    filter_dict['entry_timestamp']['end_date'] = diner_data['entry_timestamp'].head(1).item().date()

            diner_data = diner_data.groupby("meal_site")["entry_timestamp"].count()
            diner_data.rename("number of entries", inplace=True)
            bar_graph_title = helpers.construct_title(filter_dict, graph_type="bar", selected_demographic=selected_demographic)
            bar_graph = px.bar(diner_data, x = diner_data.index,\
                                    y = "number of entries", title = bar_graph_title, text_auto = True,
                                    color=diner_data.index)
            bar_graph.update_layout(showlegend=False)
            return bar_graph