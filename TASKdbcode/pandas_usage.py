#!/usr/bin/env python

#-----------------------------------------------------------------------
# pandas_usage.py
# Author: Rohan Amin and Andres Blanco Bonilla
# Tests using pandas to generate demographic stats about race
#-----------------------------------------------------------------------


from numpy import dtype
from sqlalchemy import true
from demographic_db import *
import database_constants as database
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def to_1D(series):
 return pandas.Series([x for _list in series for x in _list])

# To do: modularize coe
def demographic_distribution(demographic, meal_site = None):
    pass

def main():
    
    select_fields = ["service_timestamp", "meal_site", "race",]
    # for name, group in df.groupby("meal_site")
    # filter_dict = {"meal_site": "First Baptist Church"}
    filter_dict = {}

    df = get_patrons(select_fields, filter_dict)
    # create a data frame dictionary to store your data frames
    DataFrameDict = {elem: pandas.DataFrame() for elem in database.MEAL_SITE_OPTIONS}

    for key in DataFrameDict.keys():
        DataFrameDict[key] = df[:][df.meal_site == key]
    
  
    # for meal_site in database.MEAL_SITE_OPTIONS:
    #     print(DataFrameDict[meal_site]["race"].value_counts(normalize=True))
    #     print(DataFrameDict[meal_site]["race"].value_counts().to_string(dtype = False))
    #     print()
    
    # for meal_site in database.MEAL_SITE_OPTIONS:
    #     site_df =  DataFrameDict[meal_site]
    #     num_entries = len(site_df.index)
    #     mask_condition = site_df["race"].map(len) == 1
    #     site_df_multi = site_df[~mask_condition]
    #     site_df = site_df[mask_condition]
    #     single_counts = site_df["race"].value_counts()
    #     num_multi = len(site_df_multi.index)
    #     multi_count = pandas.Series([num_multi], ["[Other]"])
    #     summary_counts = pandas.concat([single_counts, multi_count])
    #     multi_counts = site_df_multi["race"].value_counts()
        
    #     # print percents instead of raw count
    #     summary_counts = summary_counts.map(lambda c: c / num_entries * 100)
    #     multi_counts = multi_counts.map(lambda c: c / num_entries * 100)
        
    #     print(meal_site)
    #     print("-------------------------------------------------------")
    #     print(summary_counts.to_string(dtype = False))
    #     print("\nOther Breakdown")
    #     print(multi_counts.to_string(dtype = False))
    #     print("\n\n")

    site_df = df
    # print(site_df["race"])
    # num_entries = len(site_df.index)
    # mask_condition = site_df["race"].map(len) == 1
    # print(str(site_df["race"]).split(","))
    # site_df_multi = site_df[~mask_condition]
    # site_df = site_df[mask_condition]
    # site_df[mask_condition]

        
    # print percents instead of raw count
    # summary_counts = summary_counts.map(lambda c: c / num_entries * 100)
    # multi_counts = multi_counts.map(lambda c: c / num_entries * 100)
    # summary_counts.rename(lambda x: str(x))
    # print(summary_counts)
#-----------------------------------------------------------------------
    # Pie Chart (Race)
    all_counts = site_df["race"].value_counts()
    single_index = [i for i in all_counts.index if i in database.RACE_OPTIONS]
    multi_index = [i for i in all_counts.index if i not in database.RACE_OPTIONS]
    single_counts = all_counts.filter(items = single_index)
    multi_counts = all_counts.filter(items = multi_index)
    num_multi = multi_counts.size
    multi_count = pandas.Series([num_multi], ["Other"])
    summary_counts = pandas.concat([single_counts, multi_count])
    print(summary_counts)
    specs = [[{'type':'domain'}], [{'type':'domain'}]]
    pie_charts = make_subplots(rows=2, cols=1, specs=specs)
    single_chart = go.Pie(values = summary_counts, labels = summary_counts.index,
                       title = "Races of Patrons at All Meal Sites", legendgroup=1)
    other_chart = go.Pie(values = multi_counts, labels = multi_counts.index,
                       title = "Other: Races of Multi-Racial Patrons at All Meal Sites", legendgroup=2)
    pie_charts.add_trace(single_chart, 1, 1)
    pie_charts.add_trace(other_chart, 2, 1)
    pie_charts.update_layout(legend_tracegroupgap = 180)
    pie_charts.show()

#-----------------------------------------------------------------------
    # Bar Chart All Comparison (complex demographic)
    
    filter_dict = {"homeless": "True", "veteran": "True"}
    
    filtered_data = get_patrons([], filter_dict).groupby("meal_site")["service_timestamp"].count()
    filtered_data.rename("count", inplace=True)
    print(filtered_data)
    bar_graph = px.bar(filtered_data, x = filtered_data.index,\
        y = "count", title = "Comparison of Homeless Veterans Across All Meal Sites", text_auto = True)
    bar_graph.update_layout(showlegend=False)
    
    bar_graph.show()

#-----------------------------------------------------------------------
    # Popped Out Pie Chart (complex demographic)
    
    filter_dict = {"meal_site": "Pelletier Homes", "homeless": "True", "veteran": "True"}
    
    num_entries = len(get_patrons([], {"meal_site": "Pelletier Homes"}).index)

    
    
    filtered_data = get_patrons([], filter_dict)["service_timestamp"].count()
    num_entries = num_entries - filtered_data
    filtered_data = pandas.Series([filtered_data],["Homeless Veterans"])
    other_count = pandas.Series([num_entries], ["Other"])
    #filtered_data.rename("count", inplace=True)
        #     num_multi = len(site_df_multi.index)
    #     
    filtered_data = pandas.concat([filtered_data, other_count])
    print(filtered_data)
    exp_pie_chart = go.Figure(data = [go.Pie(values = filtered_data.values, labels = filtered_data.index, pull = [0.2,0],
                                             title = "Homeless Veterans at Pelletier Homes")])
    
    exp_pie_chart.show()

#-----------------------------------------------------------------------
    # Bar Chart Pair Comparison (simple demographic)
    filter_dict1 = {"meal_site": "First Baptist Church"}
    filter_dict2 = {"meal_site": "Medallion Care Behavioral Health"}
    
    df1 = get_patrons([], filter_dict1)
    df2 = get_patrons([], filter_dict2)
    combined_df = pandas.concat([df1, df2])
    histogram = px.histogram(combined_df, x="gender",
             color='meal_site', barmode='group',
             height=400, title =\
                 "Gender of Patrons at First Baptist Church vs. Medallion Care Behavior Health")
    
    histogram.show()

#-----------------------------------------------------------------------
    # Bar Chart Comparison Single vs All (simple demographic)
    filter_dict1 = {"field": "meal_site", "op": "==", "value": "First Baptist Church"}
    filter_dict2 = {"field": "meal_site", "op": "!=", "value": "First Baptist Church"}
    
    df1 = filter_dm(filter_dict1)["gender"].value_counts()
    df2 = filter_dm(filter_dict2)
    
    num_sites = len(df.meal_site.unique())
    
    df2["meal_site"] = "Other"

    df2 = df2.groupby("gender")["service_timestamp"].count()
    print(df2)
    df2 = df2.map(lambda c: c / num_sites)

    combined_histogram = go.Figure(data=[
    go.Bar(x = df1.index, y = df1.values, name='First Baptist Church'),
    go.Bar(x = df2.index, y = df2.values, name="Average of Other Sites")])
    combined_histogram.update_layout(yaxis_title = "count", title =\
        "Gender of Patrons at First Baptist Church vs. All Other Meal Site Average", barmode="group")
    combined_histogram.show()
#-----------------------------------------------------------------------
    # Bar Chart Comparison All (simple demographic)
    df_all = get_patrons([], {})
    all_histogram = px.histogram(df_all, x="gender",
             color='meal_site', barmode='group',
             height=400, title = "Genders of Patrons at All Meal Sites")
    all_histogram.show()
    
    
    # print("All Meal Sites")
    # print("-------------------------------------------------------")
    # print(summary_counts.to_string(dtype = False))
    # print("\nOther Breakdown")
    # print(multi_counts.to_string(dtype = False))
    # print("\n\n")

    # print(DataFrameDict["First Baptist Church"])
    # firstdf = DataFrameDict["First Baptist Church"]
   

    # print(firstdfs["race"].value_counts(normalize=True).to_string(dtype = False))
    # print(to_1D(firstdf["race"]))
    # good

    # print()
    
    # print(to_1D(df["race"]).value_counts())
    
    
    
    
    
    
    
    # num_by_race = df.groupby(df["race"].map(tuple))["service_timestamp"].count()
    # print(num_by_race.head(10))

    # df[f'total_American_Indian'] = 0 
    # df[f'total_Asian'] = 0 
    # df[f'total_Black'] = 0 
    # df[f'total_Pacific_Islander'] = 0 
    # df[f'total_White'] = 0 
    # df[f'total_Hispanic'] = 0 
    # df[f'total_Unknown'] = 0 
    
    # for name, group in df.groupby("meal_site"): 
    #     df[f'{name}_American_Indian'] = 0 
    #     df[f'{name}_Asian'] = 0 
    #     df[f'{name}_Black'] = 0 
    #     df[f'{name}_Pacific_Islander'] = 0 
    #     df[f'{name}_White'] = 0 
    #     df[f'{name}_Hispanic'] = 0 
    #     df[f'{name}_Unknown'] = 0 
    #     for index, row in group.iterrows(): 
    #         for race in row["race"]: 
    #             if race == "American Indian/Alask Native": df[f'{name}_American_Indian'] += 1
    #             if race == "Asian": df[f'{name}_Asian'] += 1
    #             if race == "Black": df[f'{name}_Black'] += 1
    #             if race == "Native Hawaiian/Pacific Islander": df[f'{name}_Pacific_Islander'] += 1
    #             if race == "White": df[f'{name}_White'] +=1
    #             if race == "Hispanic": df[f'{name}_Hispanic'] +=1
    #             if race == "Unknown": df[f'{name}_Unknown'] +=1
    #     df[f'total_American_Indian'] += df[f'{name}_American_Indian']
    #     df[f'total_Asian'] +=  df[f'{name}_Asian']
    #     df[f'total_Black'] += df[f'{name}_Black']
    #     df[f'total_Pacific_Islander'] += df[f'{name}_Pacific_Islander'] 
    #     df[f'total_White'] += df[f'{name}_White'] 
    #     df[f'total_Hispanic'] += df[f'{name}_Hispanic']
    #     df[f'total_Unknown'] += df[f'{name}_Unknown'] 
    # with pandas.option_context('display.max_rows', 10, 'display.max_columns', None):  # more options can be specified also
    #     print(df)



if __name__ == "__main__": 
    main()
