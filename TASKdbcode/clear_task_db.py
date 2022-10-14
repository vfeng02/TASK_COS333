#!/usr/bin/env python

#-----------------------------------------------------------------------
# clear_task_db.py
# Author: Andres Blanco Bonilla
# Uses SQLAlchemy to clear the demographic database in ElephantSQL
# (deleting all the table data but not the tables themselves)
# for testing purposes
#-----------------------------------------------------------------------

import sys

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import func
import psycopg2

import demographic_db as database
from database_constants import DATABASE_URL

#-----------------------------------------------------------------------

def main():
    
    if len(sys.argv) != 1:
        print('Usage: python clear_task_db.py', file=sys.stderr)
        sys.exit(1)

    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        # clearing the tables like this is simple but might be slow
        # maybe find a better way to do it
        # if performance becomes an issue
        database.Base.metadata.drop_all(engine)
        database.Base.metadata.create_all(engine)
        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
