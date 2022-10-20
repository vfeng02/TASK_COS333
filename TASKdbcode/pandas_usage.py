from demographic_db import * 



if __name__ == "__main__": 
    # filters = {"race": ["American Indian/Alaska Native", "Asian", "Black",\
    # "Native Hawaiian/Pacific Islander", "White", "Hispanic",\
    #     "Unknown"]}
    select_fields = ["service_timestamp", "meal_site", "race",]

    df = get_patrons(select_fields)

    
    df[f'total_American_Indian'] = 0 
    df[f'total_Asian'] = 0 
    df[f'total_Black'] = 0 
    df[f'total_Pacific_Islander'] = 0 
    df[f'total_White'] = 0 
    df[f'total_Hispanic'] = 0 
    df[f'total_Unknown'] = 0 
    
    for name, group in df.groupby(["meal_site"]): 
        df[f'{name}_American_Indian'] = 0 
        df[f'{name}_Asian'] = 0 
        df[f'{name}_Black'] = 0 
        df[f'{name}_Pacific_Islander'] = 0 
        df[f'{name}_White'] = 0 
        df[f'{name}_Hispanic'] = 0 
        df[f'{name}_Unknown'] = 0 
        for index, row in group.iterrows(): 
            for race in row["race"]: 
                if race == "American Indian/Alask Native": df[f'{name}_American_Indian'] += 1
                if race == "Asian": df[f'{name}_Asian'] += 1
                if race == "Black": df[f'{name}_Black'] += 1
                if race == "Native Hawaiian/Pacific Islander": df[f'{name}_Pacific_Islander'] += 1
                if race == "White": df[f'{name}_White'] +=1
                if race == "Hispanic": df[f'{name}_Hispanic'] +=1
                if race == "Unknown": df[f'{name}_Unknown'] +=1
        df[f'total_American_Indian'] += df[f'{name}_American_Indian']
        df[f'total_Asian'] +=  df[f'{name}_Asian']
        df[f'total_Black'] += df[f'{name}_Black']
        df[f'total_Pacific_Islander'] += df[f'{name}_Pacific_Islander'] 
        df[f'total_White'] += df[f'{name}_White'] 
        df[f'total_Hispanic'] += df[f'{name}_Hispanic']
        df[f'total_Unknown'] += df[f'{name}_Unknown'] 


    



            

