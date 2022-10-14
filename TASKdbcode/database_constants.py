#!/usr/bin/env python

#-----------------------------------------------------------------------
# database_constants.py
# Author: Andres Blanco Bonilla
# Stores information about the TASK demographic database as constants
# for other programs to use
#-----------------------------------------------------------------------

import demographic_db as database

#-----------------------------------------------------------------------

DATABASE_URL = ("postgresql+psycopg2://usqmchwx:"
                "jVw_QrUQ-blJpl1dXhixIQmPAsD89W-R"
                "@peanut.db.elephantsql.com/usqmchwx")

DEMOGRAPHIC_OPTIONS = ["race", "ethnicity", "language", "age_range",\
                       "gender", "zip_code", "homeless", "veteran",
                       "disabled", "patron_response"]

RACE_OPTIONS = ["American Indian/Alaska Native", "Asian", "Black",\
    "Native Hawaiian/Pacific Islander", "White", "Multiracial"]

ETHNICITY_OPTIONS = ["H", "N"]

LANGUAGE_OPTIONS = ["English", "Spanish", "French"]

AGE_RANGE_OPTIONS = ["<18", "18-24", "25-34", "35-44", "45-54",\
    "55-64", ">65"]

GENDER_OPTIONS = ["M", "F", "O"]

ZIP_CODE_OPTIONS = ["08540", "08618", "08648", "08610"]

YN_OPTIONS = ["Y", "N"]

HOMELESS_OPTIONS = ["Y", "N"]

VETERAN_OPTIONS = ["Y", "N"]

DISABLED_OPTIONS = ["Y", "N"]

PATRON_RESPONSE_OPTIONS = ["Y", "N"]

MEAL_SITE_OPTIONS = [database.First_Baptist_Church,\
    database.First_Presbyterian_Church_of_Hightstown,\
    database.First_United_Methodist_Church_of_Hightstown,\
    database.Holy_Apostles_Episcopal_Church,\
    database.Medallion_Care_Behavioral_Health,\
    database.Princeton_United_Methodist_Church,\
    database.Trenton_Area_Soup_Kitchen,\
    database.Trenton_Rescue_Mission,\
    database.Trinity_Episcopal_Cathedral]