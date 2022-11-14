#!/usr/bin/env python

#-----------------------------------------------------------------------
# create_task_db.py
# Author: Andres Blanco Bonilla
# Uses SQLAlchemy to create the TASK database in ElephantSQL
# Meal site tables start empty
# User tables start with some example entries
#-----------------------------------------------------------------------

import sys

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import func
import psycopg2

import demographic_db as database
import database_constants
from database_constants import DATABASE_URL

#-----------------------------------------------------------------------

def insert_users(session):
    #-------------------------------------------------------------------

    admin = database.User(username = "jaimeparker",
                          email = "jaimep@trentonsoupkitchen.org",
                          role = "administrator")
    admin.set_password("Jaime's password")
    session.add(admin)
    session.commit()

    #-------------------------------------------------------------------

    rep = database.User(username = "charleskelly",
                        email = "charlie@fx.com",
                        role = "representative")
    rep.set_password("Charlie's password")
    session.add(rep)
    
    rep = database.User(username = "ronaldmcdonald",
                        email = "mac@fx.com",
                        role = "representative")
    rep.set_password("Mac's password")
    session.add(rep)
    
    rep = database.User(username = "dennisreynolds",
                        email = "dennis@fx.com",
                        role = "representative")
    rep.set_password("Dennis' password")
    session.add(rep)
    
    rep = database.User(username = "deandrareynolds",
                        email = "dee@fx.com",
                        role = "representative")
    rep.set_password("Dee's password")
    session.add(rep)
    
    rep = database.User(username = "franklinreynolds",
                        email = "frank@fx.com",
                        role = "representative")
    rep.set_password("Frank's password")
    session.add(rep)

    session.commit()

    #-------------------------------------------------------------------

#-----------------------------------------------------------------------

def add_entry_counts(session):
    for site in database_constants.MEAL_SITE_OPTIONS:
        entry_count = database.EntryCount(meal_site = site, num_entries = 0)
        session.add(entry_count)
    session.commit()

#-------------------------------------------------------------------

def main():

    if len(sys.argv) != 1:
        print('Usage: python create_task_db.py', file=sys.stderr)
        sys.exit(1)

    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        database.Base.metadata.drop_all(engine)
        database.Base.metadata.create_all(engine)

        with sqlalchemy.orm.Session(engine) as session:
            insert_users(session)
            add_entry_counts(session)

        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------


if __name__ == '__main__':
    main()
