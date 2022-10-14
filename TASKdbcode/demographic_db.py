#!/usr/bin/env python

#-----------------------------------------------------------------------
# demographic_database.py
# Author: Andres Blanco Bonilla
# Sets up TASK database table classes for SQLAlchemy to use
#----------------------------------------------------------------------


from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

from werkzeug.security import generate_password_hash,\
    check_password_hash


Base = declarative_base()

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

# This is the base model for every meal site table in the database
# Every meal site inherits these fields
class MealSite(AbstractConcreteBase, Base):
    service_timestamp = Column(DateTime, primary_key = True)
    race = Column(String())
    ethnicity = Column(String(1))
    language = Column(String())
    age_range = Column(String(5))
    gender = Column(String(1))
    zip_code = Column(String(5))
    homeless = Column(String(1))
    veteran = Column(String(1))
    disabled = Column(String(1))
    patron_response = Column(String(1))


class Trenton_Area_Soup_Kitchen(MealSite):
    __tablename__ = "trenton_area_soup_kitchen"
    
class First_Baptist_Church(MealSite):
    __tablename__ = "first_baptist_church"
    
class Trinity_Episcopal_Cathedral(MealSite):
    __tablename__ = "trinity_episcopal_church"

class First_United_Methodist_Church_of_Hightstown(MealSite):
    __tablename__ = "first_united_methodist_church_of_hightstown"

class First_Presbyterian_Church_of_Hightstown(MealSite):
    __tablename__ = "first_presbyterian_church_of_hightstown"
    
class Princeton_United_Methodist_Church(MealSite):
    __tablename__ = "princeton_united_methodist_church"

class Holy_Apostles_Episcopal_Church(MealSite):
    __tablename__ = "holy_apostles_episcopal_church"

class Trenton_Rescue_Mission(MealSite):
    __tablename__ = "trenton_rescue_mission"

class Medallion_Care_Behavioral_Health(MealSite):
    __tablename__ = "medallion_care_behavioral_health"


Base.registry.configure()