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
                       "disabled", "guessed"]

DEMOGRAPHIC_CATEGORIES = {"race":"Race",
                          "language":"Language",
                          "age_range":"Age Range",
                          "gender":"Gender",
                          "zip_code":"Zip Code",
                          "homeless":"Homeless Status",
                          "veteran":"Veteran Status",
                          "disabled":"Disability Status",
                          "guessed":"Guessed Entry Status"}

DEMOGRAPHIC_CATEGORIES_SWAPPED = dict([(value, key) for key, value in DEMOGRAPHIC_CATEGORIES.items()])

DEMOGRAPHIC_CATEGORY_DROPDOWN_LABELS = ["Race", "Language", "Age Range",\
                       "Gender", "Zip Code", "Homeless Status", "Veteran Status",\
                       "Disability Status", "Guessed Entry Status", "None"]

DEMOGRAPHIC_CATEGORY_DROPDOWN_VALUES = ["race", "language", "age_range",\
                       "gender", "zip_code", "homeless", "veteran",\
                       "disabled", "guessed", ""]

# Check all that apply
# Maybe display White as White/Caucasian
RACE_OPTIONS = ["American Indian/Alaska Native", "Asian", "Black",\
    "Native Hawaiian/Pacific Islander", "White", "Hispanic",\
        "Unknown"]

races = sorted(RACE_OPTIONS)

# This is for the graph apps don't worry about it
RACE_DROPDOWN_OPTIONS = ["White", "Black", "Hispanic", "Asian","American Indian/Alaska Native",\
    "Native Hawaiian/Pacific Islander", "Multiracial", "Unknown"]



# Primary language (not every language a person speaks)
LANGUAGE_OPTIONS = ["English", "Spanish", "ASL", "Arabic", "Bengali",
                    "Chinese", "Creole", "Dari", "Farsi", "French",\
                    "German", "Polish", "Russian", "Swahili", "Urdu",\
                    "Vietnamese", "Other", "Unknown"]

languages = sorted(LANGUAGE_OPTIONS)
OTHER_LANGUAGE_OPTIONS = ["ASL", "Arabic", "Bengali",\
                    "Chinese", "Creole","Dari", "Farsi", "French",\
                    "German", "Polish", "Russian", "Swahili", "Urdu",\
                    "Vietnamese", "Other", "Unknown"]

otherlanguages = sorted(OTHER_LANGUAGE_OPTIONS)

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

# Dict keys are meal sites
# and dict values are the city/town/township of the meal site
MEAL_SITE_LOCATIONS = {"First Baptist Church":"Trenton",\
    "First Presbyterian Church of Hightstown":"Hightstown",\
    "First United Methodist Church of Hightstown":"Hightstown",\
    "Holy Apostles Episcopal Church":"Trenton" ,\
    "Medallion Care Behavioral Health":"Trenton",\
    "Princeton United Methodist Church":"Princeton",\
    "Trenton Area Soup Kitchen":"Trenton",\
    "Rescue Mission":"Trenton",\
    "Trinity Episcopal Cathedral":"Trenton",\
    "Trenton Circus Squad":"Trenton",\
    "Harvest Intercontinental Ministries United":"Trenton",\
    "St James AME Church":"Hightstown",\
    "Bible Way Cathedral of Deliverance":"Trenton",\
    "Redding Circle Senior Center":"Princeton",\
    "Mercer Behavioral Health":"Ewing",\
    "Turning Point United Methodist Church":"Trenton",\
    "Princeton Family YMCA":"Princeton",\
    "Homefront":"Lawrenceville",\
    "St Lukes Church":"Ewing",\
    "Morrisville United Methodist Church":"Morrisville",\
    "Cartet Arms":"Trenton",\
    "Masjidul Taowa":"Trenton",\
    "Architects Housing":"Trenton",\
    "Louis Josephson Apartments":"Trenton",\
    "James J. Abbot Apartments": "Trenton",\
    "J. Conner French Towers": "Trenton",\
    "Luther Towers":"Trenton",\
    "Cathedral Square":"Trenton",\
    "North 25 Apartments":"Trenton",\
    "Kingsbury Towers":"Trenton",\
    "Pelletier Homes":"Trenton",\
    "Independence Gardens":"Princeton",\
    "City of Trenton Hotels":"Trenton"}

# Dict keys are a city/town/township
# and dict values are the list of corresponding zip codes
ZIP_CODES = {"Trenton": ["08608", "08609", "08610", "08611", "08618", "08629", "08638", "08648"],
             "Highstown": ["08520"],
             "Princeton": ["08540", "08542", "08544"],
             "Ewing":["08560", "08534", "08618", "08628", "08638"],
             "Morrisville": ["15370", "19067"]}

# This is just for the graph apps don't worry about it
ZIP_CODE_DROPDOWN_OPTIONS = ["08608", "08609", "08610", "08611", "08618", "08629", "08638", "08648",
                      "08520","08540", "08542", "08544","08560", "08534", "08618", "08628", "08638",
                      "15370", "19067", "Other", "Unknown"]


HOMELESS_OPTIONS = ["Yes", "No", "Unknown"]

VETERAN_OPTIONS = ["Yes", "No",  "Unknown"]

DISABLED_OPTIONS = ["Yes", "No", "Unknown"]

GUESSED_OPTIONS = ["Yes", "No"]

STATUS_OPTION_MAPPING = {"homeless":{"Yes":"Homeless", "No":"Not Homeless", "Unknown":"Unknown if Homeless"},
                         "veteran":{"Yes":"Veteran", "No":"Not Veteran", "Unknown":"Unknown if Veteran"},
                         "disabled":{"Yes":"Disabled", "No":"Not Disabled", "Unknown":"Unknown if Disabled"},
                         "guessed":{"Yes":"Entry Completely Guessed", "No":"Entry Not Guessed"}}


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