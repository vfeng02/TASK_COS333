#!/usr/bin/env python

#-----------------------------------------------------------------------
# pandas_usage.py
# Author: Rohan Amin and Andres Blanco Bonilla
# Sets up TASK database table classes for SQLAlchemy to use
#-----------------------------------------------------------------------


from numpy import dtype
from demographic_db import *
import database_constants as database

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
    
    for meal_site in database.MEAL_SITE_OPTIONS:
        site_df =  DataFrameDict[meal_site]
        mask_condition = site_df["race"].map(len) == 1
        site_df_multi = site_df[~mask_condition]
        site_df = site_df[mask_condition]
        single_counts = site_df["race"].value_counts()
        multi_count = pandas.Series([len(site_df_multi.index)], ["[Other]"])
        summary_counts = pandas.concat([single_counts, multi_count])
        multi_counts = site_df_multi["race"].value_counts()
        print(meal_site)
        print("-------------------------------------------------------")
        print(summary_counts.to_string(dtype = False))
        print("\nOther Breakdown")
        print(multi_counts.to_string(dtype = False))
        print("\n\n")
        
        


    # print(DataFrameDict["First Baptist Church"])
    firstdf = DataFrameDict["First Baptist Church"]
   

    # print(firstdfs["race"].value_counts(normalize=True).to_string(dtype = False))
    # print(to_1D(firstdf["race"]))
    # good

    print()
    
    print(to_1D(df["race"]).value_counts())
    
    
    
    
    
    
    
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
