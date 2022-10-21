
#!/usr/bin/env python
#-----------------------------------------------------------------------
# filter_db.py
# Author: Andres Blanco Bonilla
# Testing db filters
#-----------------------------------------------------------------------

import demographic_db as database
from tabulate import tabulate
import pandas

#-----------------------------------------------------------------------


def main():
    selects = ["service_timestamp", "meal_site", "race", "gender",
               "age_range"]
    filters = {"meal_site": "Trenton Area Soup Kitchen", "race": ["Hispanic"]}
    df = database.get_patrons(selects, filters)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    print(df)
#-----------------------------------------------------------------------
if __name__ == '__main__':
    main()
