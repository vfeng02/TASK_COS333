#!/usr/bin/env python

#-----------------------------------------------------------------------
# demographic_db.py
# Author: Andres Blanco Bonilla
# Sets up TASK database table classes for SQLAlchemy to use
#-----------------------------------------------------------------------

import sys
import pandas
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import functions
from TASKdbcode import database_constants
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
engine = sqlalchemy.create_engine(DATABASE_URL)

# Table for both types of users in the database
# Role will either be representative or administrator
class User(Base):
    __tablename__ = "users"
    username = Column(String(), primary_key = True)
    password_hash = Column(String())
    email = Column(String())
    role = Column(String())
    # idrk about this hashing stuff I just stole it from here
    # https://dev.to/kaelscion/authentication-hashing-in-sqlalchemy-1bem
    # need to figure out authentication later
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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

class EntryCount(Base):
    __tablename__ = "entry_counts"
    meal_site = Column(String(), primary_key = True)
    num_entries = Column(Integer())

Base.registry.configure()

#-----------------------------------------------------------------------

def add_patron(input_dict):
    
    for key in input_dict:
        if not input_dict[key]:
            if key == "language":
                input_dict[key] = "English"
            elif key == "guessed":
                input_dict[key] = "False"
            else:
                input_dict[key] = "Unknown"

    try:
        # engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # demographics = {}
            # for demographic in demographic_options:
            #     demographics[demographic] = args_dict[demographic]
            entry = MealSite(\
                entry_timestamp = sqlalchemy.func.now(),\
                    **input_dict)
            session.add(entry)
            print(input_dict)
            query = session.query(EntryCount).filter(EntryCount.meal_site == input_dict["meal_site"])
            row = query.one()
            row.num_entries += 1
            session.commit()

        # engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------
def get_last_patron(meal_site):
    try:
        # engine = sqlalchemy.create_engine(DATABASE_URL)
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(MealSite)
            filter_spec = {"field": "meal_sites", "op" : "==", "value": meal_site}
            query = query.filter_by(meal_site = meal_site)
            #.filter_by(meal_site=meal_site)
            entry = pandas.read_sql(query.statement, session.bind).tail(1)
            
        # engine.dispose()
        print(entry)
        print(type(entry))
        return entry
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------
def delete_last_patron(meal_site):
    filter_dict = {"meal_site": meal_site}
    #filter_dict2 = {"meal_site": "Medallion Care Behavioral Health"}
    filter_dict = {key:value for (key, value) in\
                   filter_dict.items() if value}
    for key, value in filter_dict.items():
        filter_spec = {"field": key, "op" : "==", "value": value}
    try:

        with sqlalchemy.orm.Session(engine) as session:
            #filter_spec = {"field": "meal_site", "op" : "==", "value": "First Baptist Church"}
            #filter_spec = {"field": key, "op" : "==", "value": value}
            obj=session.query(MealSite).filter_by(meal_site = meal_site).order_by(MealSite.entry_timestamp.desc()).first()
            #obj = session.query(MealSite).order_by(MealSite.entry_timestamp.desc()).first()
            session.delete(obj)
            query = session.query(EntryCount).filter(EntryCount.meal_site == "meal_site")
            row = query.one()
            row.num_entries -= 1

            session.commit()


    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)


#-----------------------------------------------------------------------
def get_patrons(filter_dict = {}, select_fields = []):

    filter_dict = {key:value for (key, value) in\
                   filter_dict.items() if value}
    # print(filter_dict)

    select_fields = [getattr(MealSite, field) for\
        field in select_fields]
    
    
    try:
        # engine = sqlalchemy.create_engine(DATABASE_URL)

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
                        if item == "Multiracial":
                            filter_spec["or"].append({"field": key, "op" : "ilike", "value": "%,%"})
                        elif item == "Other" and key == "zip_code":
                            filter_spec["or"].append({"field": key, "op" : "not_in", "value": database_constants.ZIP_CODE_DROPDOWN_OPTIONS})
                        else:
                            filter_spec["or"].append({"field": key, "op" : "==", "value": item})
                elif type(value) is dict:
                    filter_spec = {"and": []}
                    filter_spec["and"].append({"field": "entry_timestamp", "op": ">=", "value": value["start_date"]})
                    filter_spec["and"].append({"field": "entry_timestamp", "op": "<=", "value": value["end_date"]})
                else:
                    filter_spec = {"field": key, "op" : "==", "value": value}
                    
                query = apply_filters(query, filter_spec)
            # print(query)
            demographic_df = pandas.read_sql(query.statement, session.bind)

        # engine.dispose()
        return demographic_df

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------
def get_users(value):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            if value == 0:
                 query =session.query(User)
            if value == 1:
                 query =session.query(User).filter_by(role = "administrator")
            if value == 2:
                 query =session.query(User).filter_by(role = "representative")
            user_df = pandas.read_sql(query.statement, session.bind)
        html_code = user_df.to_html()
        return html_code
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

def filter_dms(filter_dicts):
    try:
        # engine = sqlalchemy.create_engine(DATABASE_URL)
        with sqlalchemy.orm.Session(engine) as session:
            # Keep the filters that were entered in the dict
            query = session.query(MealSite).order_by(MealSite.entry_timestamp.desc())
            if filter_dicts:
                for filter_dict in filter_dicts:
                    # or filtering
                    if type(filter_dict["value"]) is list:
                        filter_spec = {"or": []}
                        for item in filter_dict["value"]:
                            filter_spec["or"].append({"field": filter_dict["field"], "op" : filter_dict["op"], "value": item})
                    else:
                        filter_spec = filter_dict
                        
                    query = apply_filters(query, filter_spec)
            demographic_df = pandas.read_sql(query.statement, session.bind)
        # engine.dispose()
        return demographic_df
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)


def get_num_entries(meal_site):
    try:
        # engine = sqlalchemy.create_engine(DATABASE_URL)
        num_entries = 0

        with sqlalchemy.orm.Session(engine) as session:
            if type(meal_site) is list:
                query = session.query(functions.sum(EntryCount.num_entries).label("total_num")).filter(EntryCount.meal_site.in_(meal_site))
                num_entries = query.one().total_num
            else:
                query = session.query(EntryCount).filter(EntryCount.meal_site == meal_site)
                num_entries = query.one().num_entries
        # engine.dispose()
        return num_entries

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

def get_total_entries():
    
    try:
        # engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Keep the filters that were entered in the dict
            query = session.query(functions.sum(EntryCount.num_entries).label('total_num'))
            num_entries = query.one().total_num
            #print(query)
        # engine.dispose()
        return num_entries
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

# input a dict like {"username":username,
#                    "email":email
#                    "password":password.
#                    "role": role}
# role is either administrator or representative
def add_user(input_dict):
    
    if input_dict["role"] not in ["administrator", "representative"]:
        return
        # maybe do some other checks here for a "valid" username/email/password

    # print(input_dict)

    try:
        # engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # demographics = {}
            # for demographic in demographic_options:
            #     demographics[demographic] = args_dict[demographic]
            user = User(username = input_dict["username"],
                          email = input_dict["email"],
                          role = input_dict["role"])
            user.set_password(input_dict["password"])
            session.add(user)

            session.commit()

        # engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

def display_users():
    
    try:
        # engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:

                query = session.query(User)
                table = query.all()
                for row in table:
                    print("\nuser")
                    print('-------------------------------------------')
                    print(f"username: {row.username}\npassword_hash: {row.password_hash}\nrole: {row.role}\nemail:{row.email}")
                    print('-------------------------------------------')
        # engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------
    
def check_my_users(user):
    """Check if user exists and its credentials.
    """
    try:
        print(user["username"], " hello")
        with sqlalchemy.orm.Session(engine) as session:
                query = session.query(User).filter(User.username == user["username"])
                print(query)
                if not query: return False
                for row in query:
                    if check_password_hash(row.password_hash, user["password"]): 
                        return True
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# def admin_change_user_password(username, password): 
#     try: 
#         with sqlalchemy.orm.Session(engine) as session:
#                     query = session.query(User).filter(User.username == username)
#                     if not query: return False
#                     for row in query:
#                         row.password = password
#             # engine.dispose()

#     except Exception as ex:
#         print(ex, file=sys.stderr)
#         sys.exit(1)
    
# def user_change_password(username, password, new_password):
#     try:
#         with sqlalchemy.orm.Session(engine) as session:
#                 query = session.query(User).filter(User.username == username)
#                 if not query: print("User does not exist.")
#                 for row in query:
#                     if check_password_hash(row.password_hash, password): 
#                         row.password_hash = generate_password_hash(new_password)
#                         return
#                     else: 
#                         return ("Password does not match the username's password in the database")

#     except Exception as ex:
#         print(ex, file=sys.stderr)
#         sys.exit(1)

def be_admin(username):
    """Validator to check if user has admin role"""
    try:
        print(username)
        with sqlalchemy.orm.Session(engine) as session:
                query = session.query(User).filter(User.username == username)
                print(query)
                if not query: return False
                for row in query:
                    if row.role != 'administrator': 
                        return False 
                        # "User does not have admin role"
                    return
    except EOFError as ex: 
        print("there is an error in be_admin")
        sys.exit(1)
    # except Exception as ex:
    #     print(ex, file=sys.stderr)
    #     sys.exit(1)
    


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





