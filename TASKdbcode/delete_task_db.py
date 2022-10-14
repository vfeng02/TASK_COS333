#!/usr/bin/env python

#-----------------------------------------------------------------------
# delete_task_db.py
# Author: Andres Blanco Bonilla
# Uses SQLAlchemy to delete every table in the demographic database in 
# ElephantSQL for testing purposes
#-----------------------------------------------------------------------

import sys

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import func
import psycopg2

import demographic_db as database

#-----------------------------------------------------------------------

DATABASE_URL = "postgresql+psycopg2://usqmchwx:jVw_QrUQ-blJpl1dXhixIQmPAsD89W-R@peanut.db.elephantsql.com/usqmchwx"

engine = sqlalchemy.create_engine(DATABASE_URL)

def main():

    if len(sys.argv) != 1:
        print('Usage: python delete_task_db.py', file=sys.stderr)
        sys.exit(1)

    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        database.Base.metadata.drop_all(engine)
        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
