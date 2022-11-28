#!/usr/bin/env python

# -----------------------------------------------------------------------
# piedashboard.py
# Author: Andres Blanco Bonilla
# Dash app for pie chart display
# route: /pieapp
# -----------------------------------------------------------------------

"""Instantiate a Dash app."""
import datetime
import dash
import pandas
from TASKdbcode import demographic_db
from TASKdbcode import database_constants
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify as di
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from TASKdbcode import graphdashboard_helpers as helpers
import textwrap

CUSTOM_BOOTSTRAP = 'assets/bootstrap.min.css'
IFRAME_RESIZER = 'assets/iframeSizer.contentWindow.min.js'


def init_piedashboard(server):
    pie_app = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix="/pieapp/",
        # using default bootstrap style sheet, could be changed
        external_stylesheets=[CUSTOM_BOOTSTRAP])
    # ,external_scripts= [IFRAME_RESIZER])

    pie_app.layout = html.Div(
        children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H3("Create Pie Chart", style = {'color':'#FDF9CD', 'margin-top':'5px', 'font-weight':'bold'}),
                        html.Div([
                            html.Div([
                                html.Hr(style={"width": "100%", 'borderTop': '3px solid #ff911f',
                                        'borderBottom': '2px #ff911f', "opacity": "unset"}),
                                html.H4("Select Meal Sites", style={
                                    'display': 'inline-block', 'margin-right': '5px', 'color': 'white'}),
                                di(icon="material-symbols:help-outline-rounded",
                                   id="mshelp", color="white", inline=True, height=20),
                                dbc.Tooltip([html.P("Select the meal sites whose entries you want to be included in the pie chart. Data from your selected meal sites will be grouped together into one single pie chart. Clear your selection to automatically select any/all meal sites.",
                                                    style={"textAlign": "left", "marginBottom": 0})], target="mshelp", style={"width": 600}),
                                html.H5("Compile data from diners at...", style={"color": "white"})]),
                            dcc.Dropdown(id='site_options',
                                         options=[{'value': o, 'label': o}
                                                  for o in database_constants.MEAL_SITE_OPTIONS],
                                         clearable=True,
                                         multi=True,
                                         value=["Trenton Area Soup Kitchen"],
                                         placeholder="All Meal Sites"
                                         ),
                            html.Hr(style={"width": "100%", 'borderTop': '3px solid #ff911f',
                                    'borderBottom': '2px #ff911f', "opacity": "unset"}),
                            html.Div([
                                html.H4("Select Filters on Diners", style={
                                    'display': 'inline-block', 'margin-right': '5px'}),
                                di(icon="material-symbols:help-outline-rounded",
                                   id="fhelp", color="white", inline=True, height=20),
                                dbc.Tooltip([html.P("The pie chart will only include data from diners who meet the criteria of all your selected filters. Clear a filter selection to automatically include any/all options of that category.",
                                                    style={"textAlign": "left", "marginBottom": 0})], target="fhelp", style={"width": 600}),
                            ], style={'color': 'white'}),
                            html.H5("Make a chart of diners who are...", style={
                                    'color': 'white'}),
                            dbc.Row(id="filter_options", children=helpers.filter_options_helper(None, {}, "pie")),
                            html.Hr(style={"width": "100%", 'borderTop': '3px solid #ff911f',
                                    'borderBottom': '2px #ff911f', "opacity": "unset"}),
                            html.Div([
                                html.H4("Select Category for Slices", style={
                                    'display': 'inline-block', 'margin-right': '5px', 'color': 'white'}),
                                di(icon="material-symbols:help-outline-rounded",
                                   id="dchelp", color="white", inline=True, height=20),
                                dbc.Tooltip([html.P("Break down diner data by the category you select. For example, selecting Veteran Status will create slices for Veteran, Not a Veteran, and Unknown on the pie chart.",
                                                    style={"textAlign": "left", "marginBottom": 0})], target="dchelp", style={"width": 600}),
                                html.H5("Break down diners by...", style={'color': 'white'})]),
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
                            html.Hr(style={"width": "100%", 'borderTop': '3px solid #ff911f',
                                    'borderBottom': '2px #ff911f', "opacity": "unset"}),

                        ], className='menu-l'
                        )], width=4),
                    dbc.Col([
                        dcc.Graph(id='pie_chart',
                                  className='card',
                                  config={'displayModeBar': True,
                                          'displaylogo': False},
                                  style={'width': '100%', 'height': '100%',
                                         'display': 'block'}
                                  )], width=8),
                ])], fluid=True)], style={'backgroundColor': '#194f77',
                                          'height': '100%', 'width': '100%'}
    )
    # ISSUES:
    # Once graph is big, there's no way to make it small again,
    # maybe some sort of refresh message?

    # also, also, title construction needs line breaks,
    # unsure if that will decrease graph size?
    # title construction breaks when you select no filters

    # tab menu should extend all the way across the screen

    # change colors to be readable in black and white and less ugly


    init_callbacks(pie_app)
    # pie_app.enable_dev_tools(
    # dev_tools_ui=True,
    # dev_tools_serve_dev_bundles=True,)

    return pie_app.server


def init_callbacks(pie_app):

    @pie_app.callback(
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

    @pie_app.callback(
        Output('pie_chart', 'figure'),
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
    def update_pie_chart(selected_sites, r, l, a, gr, z, h, v, d, gs, n, time_range_start, time_range_end, selected_filters, mlabel):

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

        selected_fields = helpers.selected_fields_helper(
            dash.callback_context.inputs)
        filter_dict = dict(zip(selected_fields, selected_filters))

            
        print("\n")
        print(filter_dict)
        print("\n")
        selected_fields.append("entry_timestamp")

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

        if not any(filter_dict.values()) and selected_demographic == "":
            none_selected_message = helpers.graph_message("Please select filters and/or category.")
            return none_selected_message



        if selected_demographic != "":

            selected_fields.append(selected_demographic)

            if selected_sites:
                filter_dict["meal_site"] = selected_sites

                # sunburst chart testing
                # race_counts = demographic_db.get_patrons(filter_dict=filter_dict, select_fields=selected_fields)["race"].value_counts()
                # race_counts = race_counts.to_frame()
                # race_counts.rename(columns={"race": "count"}, inplace=True)

                # race_type = []
                # multi_count = 0

                # for race in race_counts["race"]:
                #     if "," in race:
                #         race_type.append("Multiracial")
                #         multi_count+=list(race_counts.loc[race_counts['race'] == race, 'count'])[0]
                #     else:
                #         race_type.append("")

                # race_type.insert(7, "")
                # races = race_counts["race"].to_list()
                # races.insert(7, "Multiracial")
                # counts = race_counts["count"].to_list()
                # counts.insert(7, multi_count)
                # print(counts[7:])
                # print(sum(counts[8:]))
                # print("\n")
                # # race_counts.loc[:,['race','count']]
                # print(races)
                # print(f"{len(races)}\n")
                # print(counts)
                # print(f"{len(counts)}\n")
                # print(race_type)
                # print(f"{len(race_type)}\n")
                # sunburst_chart = go.Figure(data = [go.Sunburst(labels = races, parents = race_type, values=counts, branchvalues="total")])
                # return sunburst_chart
#-----------------------------------------------------------------------
            if selected_demographic == "race":
                pie_chart = go.Figure()

                diner_data_df = demographic_db.get_patrons(
                    filter_dict=filter_dict, select_fields=selected_fields)
                num_entries = len(diner_data_df.index)

                if num_entries == 0:
                    none_found_message = helpers.graph_message("No entries found.")
                    return none_found_message


                if time_range_start and not time_range_end:
                    filter_dict['entry_timestamp']['end_date'] = diner_data_df['entry_timestamp'].head(1).item().date()

                pie_chart_title = helpers.construct_title(
                    filter_dict, graph_type="pie", selected_demographic=selected_demographic)

                percent_labels = [f"{option}: {value/num_entries:.2%}"
                                  for option, value in zip(
                                      diner_data_df[selected_demographic]
                                      .value_counts().index.tolist(),
                                      list(diner_data_df[selected_demographic].value_counts()))]
                for index, label in enumerate(percent_labels):
                    new_label = label
                    if "Am" in label:
                        new_label = new_label.replace(
                            "American Indian/Alaska Native", "AI/AN")
                        percent_labels[index] = new_label
                    if "Ha" in label:
                        new_label = new_label.replace(
                            "Native Hawaiian/Pacific Islander", "NHOPI")
                        percent_labels[index] = new_label

                pie_chart.add_trace(go.Pie(labels=percent_labels,
                                           values=list(
                                               diner_data_df[selected_demographic].value_counts()),
                                           texttemplate="%{label}<br>(%{value} Entries)",
                                           rotation=80, sort=False, visible=False))

                race_counts = diner_data_df["race"].value_counts()
                race_counts = race_counts.to_frame()
                race_counts.rename(
                    columns={"race": "count"}, inplace=True)
                race_counts["race"] = race_counts.index
                counts = []
                multi_count = 0
                race_labels = [race for race in race_counts["race"].to_list(
                ) if race in database_constants.RACE_OPTIONS]
                race_labels.append("Multiracial")
                for race in race_counts["race"]:
                    if race not in database_constants.RACE_OPTIONS:
                        multi_count += list(
                            race_counts.loc[race_counts['race'] == race, 'count'])[0]
                    else:
                        counts.append(
                            list(race_counts.loc[race_counts['race'] == race, 'count'])[0])
                counts.append(multi_count)

                percent_labels = [f"{option}: {value/num_entries:.2%}"
                                  for option, value in zip(
                                      race_labels,
                                      counts)]

                for index, label in enumerate(percent_labels):
                    new_label = label
                    if "Am" in label:
                        new_label = new_label.replace(
                            "American Indian/Alaska Native", "AI/AN")
                        percent_labels[index] = new_label

                    if "Ha" in label:
                        new_label = new_label.replace(
                            "Native Hawaiian/Pacific Islander", "NHOPI")
                        percent_labels[index] = new_label

                pie_chart.add_trace(go.Pie(
                    labels=percent_labels, values=counts, texttemplate="%{label}<br>(%{value} Entries)",
                    rotation=80, sort=False, visible=True))

                pie_chart.update_layout(
                    legend={"xanchor": "left",
                            "x": 1,
                            "yanchor": "top",
                            "y": 1})

                pie_chart.update_layout(
                    updatemenus=[
                        dict(
                            type="dropdown",
                            direction="down",
                            active=0,
                            showactive=True,
                            x=0.75,
                            y=0.99,
                            xanchor="left",
                            yanchor="top",
                            buttons=list([
                                dict(label="Group Multiracial",
                                     method="restyle",
                                     args=[{"visible": [False, True]}, ]),
                                dict(label="Split Multiracial",
                                     method="restyle",
                                     args=[{"visible": [True, False]}, ]),
                            ]),
                        )
                    ],
                    title=pie_chart_title)
                    # ,height=1000)
                # margin = {"t":5,"b":5,"l":5,"r":5})

                return pie_chart
#-----------------------------------------------------------------------

            diner_data_df = demographic_db.get_patrons(
                filter_dict=filter_dict, select_fields=selected_fields)

            num_entries = len(diner_data_df.index)

            if num_entries == 0:
                none_found_message = helpers.graph_message("No entries found.")
                return none_found_message

            if time_range_start and not time_range_end:
                    filter_dict['entry_timestamp']['end_date'] = diner_data['entry_timestamp'].head(1).item().date()
            
            if selected_demographic in list(database_constants.STATUS_OPTION_MAPPING.keys()):
                percent_labels = [f"{option} ({database_constants.STATUS_OPTION_MAPPING[selected_demographic][option]}): {value/num_entries:.2%}"
                              for option, value in zip(
                                  diner_data_df[selected_demographic]
                                  .value_counts().index.tolist(),
                                  list(diner_data_df[selected_demographic].value_counts()))]
            else:
                percent_labels = [f"{option}: {value/num_entries:.2%}"
                              for option, value in zip(
                                  diner_data_df[selected_demographic]
                                  .value_counts().index.tolist(),
                                  list(diner_data_df[selected_demographic].value_counts()))]

            pie_chart = go.Figure(data=[go.Pie(labels=percent_labels,
                                                values=list(
                                                    diner_data_df[selected_demographic].value_counts()),
                                                texttemplate="%{label}<br>(%{value} Entries)")])

            pie_chart_title = helpers.construct_title(
                filter_dict, graph_type="pie", selected_demographic=selected_demographic)
            pie_chart.update_layout(title=pie_chart_title)
            # pie_chart.update_traces(textposition='inside')
            # pie_chart.update_layout(uniformtext_minsize=9, uniformtext_mode='hide')
            return pie_chart

        else:

            if selected_sites:
                filter_dict["meal_site"] = selected_sites
                num_entries = demographic_db.get_num_entries(
                    selected_sites)
            else:
                num_entries = demographic_db.get_total_entries()


            diner_data = demographic_db.get_patrons(
                filter_dict=filter_dict, select_fields=selected_fields)

            if len(diner_data.index) == 0:
                none_found_message = helpers.graph_message("No entries found.")
                return none_found_message
            
            if time_range_start and not time_range_end:
                    filter_dict['entry_timestamp']['end_date'] = diner_data['entry_timestamp'].head(1).item().date()

            diner_data = diner_data["entry_timestamp"].count()

            num_other_entries = num_entries - diner_data
            filtered_slice_title = helpers.construct_slice_title(
                filter_dict=filter_dict)
            diner_data = pandas.Series(
                [diner_data], [filtered_slice_title])
            other_count = pandas.Series([num_other_entries], ["Other"])
            diner_data = pandas.concat([diner_data, other_count])
            percent_labels = [f"{option}: {value/num_entries:.2%}" for option,
                              value in zip(diner_data.index, diner_data.values)]
            exp_pie_chart = go.Figure(data=[go.Pie(labels=percent_labels, values=diner_data.values,
                                      texttemplate="%{label}<br>(%{value} Entries)", pull=[0.2, 0], rotation=295)])
            exp_pie_chart_title = helpers.construct_title(
                filter_dict, graph_type="pie", selected_demographic=selected_demographic)
            exp_pie_chart.update_layout(title=exp_pie_chart_title)
            return exp_pie_chart
