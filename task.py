#!/usr/bin/env python

#-----------------------------------------------------------------------
# task.py
# Author: Vicky Feng and Andres Blanco Bonilla
# Runs simple HTML form to input data into the TASK demographic database
#-----------------------------------------------------------------------

from ctypes import set_errno
from dis import dis
import time
from flask import Flask, request
from flask import render_template, make_response
# sys.path.insert(0, 'TASKdbcode')
# sys.path.insert(0, 'TASKfrontend/templates')
from TASKdbcode import database_constants
from TASKdbcode import demographic_db
from TASKdbcode import dashboard
# from database_constants import mealsites, languages, races, ages, genders, zip_codes
# from database_constants import HOMELESS_OPTIONS
import psycopg2

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')

#-----------------------------------------------------------------------

def get_ampm():
    if time.strftime('%p') == "AM":
        return 'morning'
    return 'afternoon'

def get_current_time():
    return time.asctime(time.localtime())

 #-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = render_template('index.html',
    ampm=get_ampm(),
    current_time=get_current_time())
    response = make_response(html_code)
    return response

 #-----------------------------------------------------------------------

@app.route('/selectmealsite', methods=['GET'])
def selectmealsite():

    html_code = render_template('selectmealsite.html',
        ampm=get_ampm(),
        current_time=get_current_time(),
        mealsites = database_constants.mealsites)

    mealsite = request.args.get('mealsite')

    response = make_response(html_code)
    # if mealsite is not None:
    #     response.set_cookie('mealsite', mealsite)
    #     print("select mealsite" + mealsite)
    # else:
    #     response.set_cookie('mealsite', '')
    return response
 #-----------------------------------------------------------------------

@app.route('/submitpatrondata', methods=['GET'])
def submitpatrondata():
    # mealsite = request.args.get('mealsite')
    new_mealsite = request.args.get('mealsite')
    mealsite = request.cookies.get('mealsite')

    set_new_mealsite = False
    
    if mealsite is None or (mealsite != new_mealsite and new_mealsite is not None): 
        set_new_mealsite = True
        mealsite = new_mealsite
        
    print(mealsite)

    race = request.args.get('race')
    language = request.args.get('language')
    age_range = request.args.get('age_range')
    gender = request.args.get('gender')
    zip_code = request.args.get('zip_code')
    homeless = request.args.get('homeless')
    veteran = request.args.get('veteran')
    disabled = request.args.get('disabled')
    patron_response = request.args.get('patron_response')

    patron_data = {"meal_site": mealsite, "race": race, "language": language,
    "age_range": age_range, "gender": gender, "zip_code": zip_code, 
    "homeless": homeless, "veteran": veteran, "disabled": disabled,
    "patron_response": patron_response}

    # demographic_db.add_patron(patron_data)
    
    print(patron_data)

    html_code = render_template('submitpatrondata.html',
        ampm=get_ampm(),
        current_time=get_current_time(),
        languages = database_constants.languages,
        races = database_constants.races,
        ages = database_constants.ages,
        genders = database_constants.genders,
        zip_codes = database_constants.ZIP_CODE_OPTIONS,
        homeless_options = database_constants.HOMELESS_OPTIONS,
        veteran_options = database_constants.VETERAN_OPTIONS,
        disabled_options = database_constants.DISABLED_OPTIONS,
        patron_response_options = database_constants.PATRON_RESPONSE_OPTIONS
        )
    response = make_response(html_code)

    if set_new_mealsite:
        response.set_cookie('mealsite', mealsite)
    return response

 #-----------------------------------------------------------------------

app = dashboard.init_dashboard(app)
@app.route('/admin', methods=['GET'])
def admindisplaydata():
    global app
    dashapp = render_template(
        "admin.html",
        title="Test",
        description="Embed Plotly Dash into your Flask applications.",
        template="home-template",
        body="This is a homepage served with Flask.",
    )
    app = Flask(__name__, template_folder='templates')
    return dashapp

    # selects = ["service_timestamp", "meal_site", "race", "gender",
    #            "age_range"]
    # filters = {"meal_site": "First Baptist Church"}
    # df = demographic_db.get_patrons(selects, filters)

    # html_code = render_template('admindisplaydata.html',
    #     ampm=get_ampm(),
    #     current_time=get_current_time(),
    #     data = df)

    # response = make_response(html_code)
    # return response


 #-----------------------------------------------------------------------

# @app.route('/submitresult', methods=['GET'])
# def submit_result():
#     name = flask.request.args.get('name')
#     if name is None:
#         name = ''
#         name = name.strip()

#     if name == '':
#         prev_name = '(None)'
#     else:
#         prev_name = name

#     # add_patron()
#         # submit name to the db

#     html_code = flask.render_template('submitresult.html',
#         ampm=get_ampm(),
#         current_time=get_current_time(),
#         name=prev_name)
#     response = flask.make_response(html_code)
#     response.set_cookie('prev_name', prev_name)
#     return response

 #-----------------------------------------------------------------------

# def submit_data():
#     try:
#         up.uses_netloc.append("postgres")
#         url = up.urlparse(os.environ["DATABASE_URL"])
#         with psycopg2.connect(database=url.path[1:],
#             user=url.username,
#             password=url.password,
#             host=url.hostname,
#             port=url.port
#             ) as connection:
#                 with contextlib.closing(connection.cursor()) as cursor:
#                     cursor.execute("PRAGMA case_sensitive_like=OFF")
#                     stmt_str ="SELECT classid, dept, coursenum, area, title"
#                     stmt_str += " FROM courses, classes, crosslistings "
#                     stmt_str += "WHERE classes.courseid = courses.courseid "
#                     stmt_str += "AND courses.courseid = "
#                     stmt_str += "crosslistings.courseid "
#                     arr = []
#     except Exception as ex:
#         #print(sys.argv[0] + ": " + str(ex), file=sys.stderr)
#         return False, None