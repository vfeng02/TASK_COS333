#!/usr/bin/env python

#-----------------------------------------------------------------------
# udisplay.py
# Author: Andres Blanco Bonilla
# Prints the contents of all the meal site tables in the TASK database
#-----------------------------------------------------------------------

from TASKdbcode import demographic_db

def main():
    # demographic_db.add_user({"username": "thewaitress2",
    #                          "password": "Waitress' password",
    #                          "": "waitress@fx.com",
    #                          "role": "representative"})
    demographic_db.display_users()

#-----------------------------------------------------------------------
if __name__ == '__main__':
    main()