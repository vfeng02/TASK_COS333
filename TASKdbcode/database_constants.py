#!/usr/bin/env python

#-----------------------------------------------------------------------
# database_constants.py
# Author: Andres Blanco Bonilla
# Stores information about the TASK demographic database as constants
# for other programs to use
#-----------------------------------------------------------------------

# import demographic_db as database

#-----------------------------------------------------------------------

DATABASE_URL = ("postgresql+psycopg2://usqmchwx:"
                "jVw_QrUQ-blJpl1dXhixIQmPAsD89W-R"
                "@peanut.db.elephantsql.com/usqmchwx")

DEMOGRAPHIC_OPTIONS = ["race", "language", "age_range",\
                       "gender", "zip_code", "homeless", "veteran",\
                       "disabled", "patron_response"]

# Check all that apply
RACE_OPTIONS = ["American Indian/Alaska Native", "Asian", "Black",\
    "Native Hawaiian/Pacific Islander", "White", "Hispanic",\
        "Unknown"]

races = sorted(RACE_OPTIONS)

# Primary language (not every language a person speaks)
LANGUAGE_OPTIONS = ["English", "Spanish", "ASL", "Arabic", "Bengali",
                    "Chinese", "Creole", "Dari", "Farsi", "French",\
                    "German", "Polish", "Russian", "Swahili", "Urdu",\
                    "Vietnamese", "Other", "Unknown"]

languages = sorted(LANGUAGE_OPTIONS)

AGE_RANGE_OPTIONS = ["<18", "18-24", "25-34", "35-44", "45-54",\
    "55-64", ">65", "Unknown"]

ages = sorted(AGE_RANGE_OPTIONS)

GENDER_OPTIONS = ["Male", "Female", "Non-Binary", "TransMale", 
                  "TransFemale", "Other", "Unknown"]

genders = sorted(GENDER_OPTIONS)
# These are not all the zip_code options
# Zip codes primarily come from Mercer County and Heightstown
# but they could be anything
ZIP_CODE_OPTIONS = ["08540", "08618", "08648", "08610", "Unknown"]

zip_codes = sorted(ZIP_CODE_OPTIONS)

HOMELESS_OPTIONS = ["True", "False", "Unknown"]

VETERAN_OPTIONS = ["True", "False", "Unknown"]

DISABLED_OPTIONS = ["True", "False", "Unknown"]

PATRON_RESPONSE_OPTIONS = [True, False]


MEAL_SITE_OPTIONS = ["First Baptist Church",\
    "First Presbyterian Church of Hightstown",\
    "First United Methodist Church of Hightstown",\
    "Holy Apostles Episcopal Church",\
    "Medallion Care Behavioral Health",\
    "Princeton United Methodist Church",\
    "Trenton Area Soup Kitchen",\
    "Rescue Mission",\
    "Trinity Episcopal Cathedral",\
    "Trenton Circus Squad",\
    "Harvest Intercontinental Ministries United",\
    "St James AME Church",\
    "Bible Way Cathedral of Deliverance",\
    "Redding Circle Senior Center",\
    "Mercer Behavioral Health",\
    "Turning Point United Methodist Church",\
    "Princeton Family YMCA",\
    "Homefront",\
    "St Lukes Church",\
    "Morrisville United Methodist Church",\
    "Cartet Arms",\
    "Masjidul Taowa",\
    "Architects Housing",\
    "Louis Josephson Apartments",\
    "James J. Abbot Apartments",\
    "J. Conner French Towers",\
    "Luther Towers",\
    "Cathedral Square",\
    "North 25 Apartments",\
    "Kingsbury Towers",\
    "Pelletier Homes",\
    "Independence Gardens",\
    "City of Trenton Hotels"]

mealsites = sorted(MEAL_SITE_OPTIONS)