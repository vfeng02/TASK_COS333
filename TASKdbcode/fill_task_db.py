#!/usr/bin/env python
#-----------------------------------------------------------------------
# fill_task_db.py
# Author: Andres Blanco Bonilla
# Randomly generates and adds the requested number of demographic
# entries into each meal site table of the database.
#-----------------------------------------------------------------------

import random
import argparse
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import func
import sys

import demographic_db as database

#-----------------------------------------------------------------------

DATABASE_URL = ("postgresql+psycopg2://usqmchwx:"
                "jVw_QrUQ-blJpl1dXhixIQmPAsD89W-R"
                "@peanut.db.elephantsql.com/usqmchwx")

# have to capitalize these, they should be constants
race_options = ["American Indian/Alaska Native", "Asian", "Black",\
    "Native Hawaiian/Pacific Islander", "White", "Multiracial"]
ethnicity_options = ["H", "N"]
language_options = ["English", "Spanish", "French"]
age_range_options = ["<18", "18-24", "25-34", "35-44", "45-54",\
    "55-64", ">65"]
gender_options = ["M", "F", "O"]
zip_code_options = ["08540", "08618", "08648", "08610"]
homeless_options = ["Y", "N"]
veteran_options = ["Y", "N"]
disabled_options = ["Y", "N"]
patron_response_options = ["Y", "N"]
table__options = [database.First_Baptist_Church,\
    database.First_Presbyterian_Church_of_Hightstown,\
    database.First_United_Methodist_Church_of_Hightstown,\
    database.Holy_Apostles_Episcopal_Church,\
    database.Medallion_Care_Behavioral_Health,\
    database.Princeton_United_Methodist_Church,\
    database.Trenton_Area_Soup_Kitchen,\
    database.Trenton_Rescue_Mission,\
    database.Trinity_Episcopal_Cathedral]

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
    entries = args_dict["number"]
    fill_db(entries)
    sys.exit(0)

def fill_db(entries):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            for table in table__options:
                for _ in range(entries):
                    random_fields = generate_demographics()
                    
                    row = table(service_timestamp = func.now(),
                          race = random_fields["race"],\
                          ethnicity = random_fields["ethnicity"],\
                          language = random_fields["language"],\
                          age_range = random_fields["age_range"],\
                          gender = random_fields["gender"],\
                          zip_code = random_fields["zip_code"],\
                          homeless = random_fields["homeless"],\
                          veteran = random_fields["veteran"],\
                          disabled = random_fields["disabled"],\
                          patron_response = random_fields\
                              ["patron_response"])
                    session.add(row)
                    session.commit()
                
        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

def generate_demographics():
    random_fields = {}
    random_fields["race"] = random.choice(race_options)
    random_fields["ethnicity"] = random.choice(ethnicity_options)
    random_fields["language"] = random.choice(language_options)
    random_fields["age_range"] = random.choice(age_range_options)
    random_fields["gender"] = random.choice(gender_options)
    random_fields["zip_code"] = random.choice(zip_code_options)
    random_fields["homeless"] = random.choice(homeless_options)
    random_fields["veteran"] = random.choice(veteran_options)
    random_fields["disabled"] = random.choice(disabled_options)
    random_fields["patron_response"] = random.choice\
        (patron_response_options)
    return random_fields

#-----------------------------------------------------------------------
if __name__ == "__main__": 
    main()