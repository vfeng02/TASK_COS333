#!/usr/bin/env python

#-----------------------------------------------------------------------
# demographic_database.py
# Author: Andres Blanco Bonilla
# Sets up TASK database table classes for SQLAlchemy to use
#-----------------------------------------------------------------------

import sys
import pandas
import sqlalchemy
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
# sql_alchemy filters has to be downloaded from this repo
# https://github.com/bodik/sqlalchemy-filters
from sqlalchemy_filters import apply_filters
# from TASKdbcode import database_constants

from werkzeug.security import generate_password_hash,\
    check_password_hash


Base = declarative_base()

DATABASE_URL = ("postgresql+psycopg2://usqmchwx:"
                "jVw_QrUQ-blJpl1dXhixIQmPAsD89W-R"
                "@peanut.db.elephantsql.com/usqmchwx")

# This is the base model for both types of Users in the database
# Both types of Users inherit these fields
class User(AbstractConcreteBase, Base):
    id = Column(Integer, primary_key=True)
    name = Column(String())
    password_hash = Column(String())
    # idrk about this hashing stuff I just stole it from here
    # https://dev.to/kaelscion/authentication-hashing-in-sqlalchemy-1bem
    # need to figure out authentication later
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Representatives(User):
    __tablename__ = "representatives"
    
class Administrators(User):
    __tablename__ = "administrators"

# Big table that stores info about every patron at every meal site
# The primary key is the timestamp + the meal site name
class MealSite(Base):
    __tablename__ = "meal_sites"
    entry_timestamp = Column(DateTime, primary_key = True)
    meal_site = Column(String(), primary_key = True)
    race = Column(String())
    language = Column(String())
    age_range = Column(String(7))
    gender = Column(String())
    zip_code = Column(String(7))
    homeless = Column(String(7))
    veteran = Column(String(7))
    disabled = Column(String(7))
    guessed = Column(String(5))

Base.registry.configure()
#-----------------------------------------------------------------------

def add_patron(input_dict):
    
    for key in input_dict:
        if key == "language" and not input_dict[key]:
            input_dict[key] = "English"

        if not input_dict[key] and key != "patron_response":
            input_dict[key] = "Unknown"

    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # demographics = {}
            # for demographic in demographic_options:
            #     demographics[demographic] = args_dict[demographic]
            entry = MealSite(\
                entry_timestamp = sqlalchemy.func.now(),\
                    **input_dict)
            session.add(entry)
            session.commit()

        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

def get_patrons(filter_dict = {}, select_fields = []):

    filter_dict = {key:value for (key, value) in\
                   filter_dict.items() if value}

    select_fields = [getattr(MealSite, field) for\
        field in select_fields]
    
    
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Keep the filters that were entered in the dict
            if (select_fields):
                query = session.query(*select_fields)
            else:
                query = session.query(MealSite)
                
            for key, value in filter_dict.items():
                if type(value) is list:
                    filter_spec = {"or": []}
                    for item in value:
                        filter_spec["or"].append({"field": key, "op" : "==", "value": item})
                else:
                    filter_spec = {"field": key, "op" : "==", "value": value}
                    
                query = apply_filters(query, filter_spec)
            # print(query)
            demographic_df = pandas.read_sql(query.statement, session.bind)

        engine.dispose()
        return demographic_df

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

def filter_dms(filter_dicts):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Keep the filters that were entered in the dict
            query = session.query(MealSite).order_by(MealSite.entry_timestamp.desc())
            if filter_dicts:
                for filter_dict in filter_dicts:
                    query = apply_filters(query, filter_dict)
            demographic_df = pandas.read_sql(query.statement, session.bind)
        engine.dispose()
        return demographic_df
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

    pass

# class Trenton_Area_Soup_Kitchen(MealSite):
#     __tablename__ = "trenton_area_soup_kitchen"
    
# class First_Baptist_Church(MealSite):
#     __tablename__ = "first_baptist_church"
    
# class Trinity_Episcopal_Cathedral(MealSite):
#     __tablename__ = "trinity_episcopal_church"

# class First_United_Methodist_Church_of_Hightstown(MealSite):
#     __tablename__ = "first_united_methodist_church_of_hightstown"

# class First_Presbyterian_Church_of_Hightstown(MealSite):
#     __tablename__ = "first_presbyterian_church_of_hightstown"
    
# class Princeton_United_Methodist_Church(MealSite):
#     __tablename__ = "princeton_united_methodist_church"

# class Holy_Apostles_Episcopal_Church(MealSite):
#     __tablename__ = "holy_apostles_episcopal_church"

# class Rescue_Mission(MealSite):
#     __tablename__ = "rescue_mission"

# class Medallion_Care_Behavioral_Health(MealSite):
#     __tablename__ = "medallion_care_behavioral_health"
    
# class Trenton_Circus_Squad(MealSite):
#     __tablename__ = "trenton_circus_squad"
    
# class Harvest_Intercontinental_Ministries_United(MealSite):
#     __tablename__ = "harvest_intercontinental_ministries_united"

# class St_James_AME_Church(MealSite):
#     __tablename__ = "st_james_ame_church"

# class Bible_Way_Cathedral_of_Deliverance(MealSite):
#     __tablename__ = "bible_way_cathedral_of_deliverance"

# class Redding_Circle_Senior_Center(MealSite):
#     __tablename__ = "redding_circle_senior_center"

# class Mercer_Behavioral_Health(MealSite):
#     __tablename__ = "mercer_behavioral_health"

# class Turning_Point_United_Methodist_Church(MealSite):
#     __tablename__ = "turning_point_united_methodist_church"

# class Princeton_Family_YMCA(MealSite):
#     __tablename__ = "princeton_family_ymca"

# class St_Lukes_Church(MealSite):
#     __tablename__ = "st_lukes_church"

# class Morrisville_United_Methodist_Church(MealSite):
#     __tablename__ = "morrisville_united_methodist_church"

# class Cartet_Arms(MealSite):
#     __tablename__ = "cartet_arms"

# class Masjidul_Taowa(MealSite):
#     __tablename__ = "masjidul_taowa"


