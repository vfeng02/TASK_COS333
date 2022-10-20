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

RACE_OPTIONS = ["American Indian/Alaska Native", "Asian", "Black",\
    "Native Hawaiian/Pacific Islander", "White", "Hispanic",\
        "Unknown"]

LANGUAGE_OPTIONS = ["English", "Spanish", "ASL", "Arabic", "Bengali",
                    "Chinese", "Creole", "Dari", "Farsi", "French",\
                    "German", "Polish", "Russian", "Swahili", "Urdu",\
                    "Vietnamese", "Other"]

AGE_RANGE_OPTIONS = ["<18", "18-24", "25-34", "35-44", "45-54",\
    "55-64", ">65", "Unknown"]

GENDER_OPTIONS = ["Male", "Female", "Non-Binary", "TransMale", 
                  "TransFemale", "Other"]

ZIP_CODE_OPTIONS = ["08540", "08618", "08648", "08610", "00000"]

HOMELESS_OPTIONS = [True, False]

VETERAN_OPTIONS = [True, False]

DISABLED_OPTIONS = [True, False]

PATRON_RESPONSE_OPTIONS = [True, False]


MEAL_SITE_OPTIONS = ["First_Baptist_Church",\
    "First_Presbyterian_Church_of_Hightstown",\
    "First_United_Methodist_Church_of_Hightstown",\
    "Holy_Apostles_Episcopal_Church",\
    "Medallion_Care_Behavioral_Health",\
    "Princeton_United_Methodist_Church",\
    "Trenton_Area_Soup_Kitchen",\
    "Rescue_Mission",\
    "Trinity_Episcopal_Cathedral",\
    "Trenton_Circus_Squad",\
    "Harvest_Intercontinental_Ministries_United",\
    "St_James_AME_Church",\
    "Bible_Way_Cathedral_of_Deliverance",\
    "Redding_Circle_Senior_Center",\
    "Mercer_Behavioral_Health",\
    "Turning_Point_United_Methodist_Church",\
    "Princeton_Family_YMCA",\
    "St_Lukes_Church",\
    "Morrisville_United_Methodist_Church",\
    "Cartet_Arms",\
    "Masjidul_Taowa"]