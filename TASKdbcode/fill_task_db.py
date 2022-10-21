#!/usr/bin/env python
#-----------------------------------------------------------------------
# fill_task_db.py
# Author: Andres Blanco Bonilla
# Randomly generates and adds the requested number of demographic
# entries into each meal site table of the TASK database
#-----------------------------------------------------------------------

import random
import argparse
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import func
import sys

import demographic_db as database
import database_constants

#-----------------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Fills the demographic database with random entries"
        , allow_abbrev=False
    )
    
    parser.add_argument(
        "number", type = int,
        metavar = "number",
        help = "The number of random entries to enter into each site",
    )
    
    args = parser.parse_args()
    args_dict = vars(args)
    num_entries = args_dict["number"]
    fill_db(num_entries)
    sys.exit(0)

def fill_db(num_entries):
    try:
        engine = sqlalchemy.create_engine(\
            database_constants.DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            for meal_site_option in database_constants.MEAL_SITE_OPTIONS:
                for _ in range(num_entries):
                    random_fields = generate_demographics()
                    
                    row = database.MealSite(service_timestamp = func.now(),\
                        meal_site = meal_site_option,
                        **random_fields)

                    session.add(row)
                    session.commit()
                
        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

def generate_demographics():
    random_fields = {}
    
    for demographic in database_constants.DEMOGRAPHIC_OPTIONS:
        options_string = demographic.upper() + "_OPTIONS"
        if demographic == "race":
            race_options = getattr(database_constants, options_string)
            num_races = random.randint(1, 2)
            random_fields[demographic] = random.sample(race_options,\
                num_races)
            if "Unknown" in random_fields[demographic]\
                and num_races > 1:
                random_fields[demographic].remove("Unknown")
        else:
            random_fields[demographic] = random.choice\
            (getattr(database_constants, options_string))

    return random_fields

#-----------------------------------------------------------------------
if __name__ == "__main__": 
    main()