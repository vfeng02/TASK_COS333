#!/usr/bin/env python

#-----------------------------------------------------------------------
# display.py
# Author: Andres Blanco Bonilla
# Prints the contents of all the meal site tables in the TASK database
#-----------------------------------------------------------------------

import sys
import sqlalchemy
import sqlalchemy.orm
import psycopg2

import demographic_db as database
from database_constants import DATABASE_URL
from database_constants import MEAL_SITE_OPTIONS
from database_constants import DEMOGRAPHIC_OPTIONS


#-----------------------------------------------------------------------


def main():

    if len(sys.argv) != 1:
        print('Usage: python display.py', file=sys.stderr)
        sys.exit(1)

    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
                print('-------------------------------------------')
                print("meal_sites")
                print('-------------------------------------------')
                query = session.query(database.MealSite)
                table = query.all()
                for row in table:
                    demographics = []
                    for demographic in DEMOGRAPHIC_OPTIONS:
                        demographics.append(getattr(row, demographic))
                    print(row.service_timestamp, row.meal_site,\
                        *demographics)

        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------


if __name__ == '__main__':
    main()
