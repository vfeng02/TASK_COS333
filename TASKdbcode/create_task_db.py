#!/usr/bin/env python

#-----------------------------------------------------------------------
# create_task_db.py
# Author: Andres Blanco Bonilla
# Uses SQLAlchemy to create the demographic database in ElephantSQL
#-----------------------------------------------------------------------

import sys

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import func
import psycopg2

import demographic_db as database

#-----------------------------------------------------------------------

DATABASE_URL = ("postgresql+psycopg2://usqmchwx:"
                "jVw_QrUQ-blJpl1dXhixIQmPAsD89W-R"
                "@peanut.db.elephantsql.com/usqmchwx")



def test_insert(session):
    #-------------------------------------------------------------------

    admin = database.Administrators(id="1234",
                                    name="Jaime Parker")
    admin.set_password("Jaime's password")
    session.add(admin)
    session.commit()

    #-------------------------------------------------------------------

    rep = database.Representatives(id="5678",
                                   name="Charlie Kelly")
    rep.set_password("Charlie's password")
    session.add(rep)

    rep = database.Representatives(id="8912",
                                   name="Ronald McDonald")
    rep.set_password("Mac's password")
    session.add(rep)

    rep = database.Representatives(id="3456",
                                   name="Dennis Reynolds")
    rep.set_password("Dennis' password")
    session.add(rep)

    rep = database.Representatives(id="6789",
                                   name="Dee Reynolds")
    rep.set_password("Dee's password")
    session.add(rep)

    rep = database.Representatives(id="1234",
                                   name="Frank Reynolds")
    rep.set_password("Frank's password")
    session.add(rep)

    session.commit()

    #-------------------------------------------------------------------

    task = database.Trenton_Area_Soup_Kitchen(
        service_timestamp=func.now(),
        race="W", ethnicity="H",
        language="English", age_range="20-24",
        gender="M", zip_code="08610", homeless="N",
        veteran="N", disabled="N", patron_response="Y")
    session.add(task)
    session.commit()

    #-------------------------------------------------------------------

    # first_baptist = database.First_Baptist_Church()
    # session.add(first_baptist)
    # session.commit()

    #-------------------------------------------------------------------

    # trinity = database.Trinity_Episcopal_Cathedral()
    # session.add(trinity)
    # session.commit()

    #-------------------------------------------------------------------

    # first_united = database.\
        # First_United_Methodist_Church_of_Hightstown()
    # session.add(first_united)
    # session.commit()

    #-------------------------------------------------------------------

    # first_pres = database.First_Presbyterian_Church_of_Hightstown()
    # session.add(first_pres)
    # session.commit()

    #-------------------------------------------------------------------

    # princeton_united = database.Princeton_United_Methodist_Church()
    # session.add(princeton_united)
    # session.commit()

    #-------------------------------------------------------------------

    # holy_apostles = database.Holy_Apostles_Episcopal_Church()
    # session.add(holy_apostles)
    # session.commit()

    #-------------------------------------------------------------------

    # trenton_rescue = database.Trenton_Rescue_Mission()
    # session.add(trenton_rescue)
    # session.commit()

    #-------------------------------------------------------------------

    # medallion_care = database.Medallion_Care_Behavioral_Health()
    # session.add(medallion_care)
    # session.commit()

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
            test_insert(session)

        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# -----------------------------------------------------------------------


if __name__ == '__main__':
    main()
