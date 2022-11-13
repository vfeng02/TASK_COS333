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
from TASKdbcode import piedashboard
from TASKdbcode import bardashboard

# from database_constants import mealsites, languages, races, ages, genders, zip_codes
# from database_constants import HOMELESS_OPTIONS
import psycopg2
from flask_simplelogin import SimpleLogin, get_username, login_required, is_logged_in


#----------------------------------------------------------------------
my_users = {
    "chuck": {"password": "norris", "roles": "admin"},
    "lee": {"password": "douglas", "roles": ""},
    "mary": {"password": "jane", "roles": ""},
    "steven": {"password": "wilson", "roles": "admin"},
}

def be_admin(username):
    """Validator to check if user has admin role"""
    user_data = my_users.get(username)
    if 'admin' not in user_data.get('roles'):
        return "User does not have admin role"

def check_my_users(user):
    """Check if user exists and its credentials.
    Take a look at encrypt_app.py and encrypt_cli.py
     to see how to encrypt passwords
    """
    user_data = my_users.get(user["username"])
    if not user_data:
        return False  # <--- invalid credentials
    elif user_data.get("password") == user["password"]:
        return True  # <--- user is logged in!

    return False  # <--- invalid credentials
#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')
with app.app_context():
        app = dashboard.init_dashboard(app)
        app = piedashboard.init_piedashboard(app)
        app = bardashboard.init_bardashboard(app)
        SimpleLogin(app, login_checker=check_my_users)
        app.config["SECRET_KEY"] = "andresallisonvickyrohan"

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
@login_required(basic=True)
def index():
    html_code = render_template('index.html',
    ampm=get_ampm(),
    current_time=get_current_time())
    response = make_response(html_code)
    return response

 #-----------------------------------------------------------------------

@app.route('/selectmealsite', methods=['GET'])
@login_required(basic=True)
def selectmealsite():

    html_code = render_template('selectmealsite.html',
        ampm=get_ampm(),
        current_time=get_current_time(),
        mealsites = database_constants.mealsites)

    response = make_response(html_code)
    return response
 #-----------------------------------------------------------------------

@app.route('/submitpatrondata', methods=['GET'])
def submitpatrondata():
    # mealsite = request.args.get('mealsite')
    new_mealsite = request.args.get('mealsite')
    mealsite = request.cookies.get('site')

    set_new_mealsite = False
    
            
    print("selected site")
    print(new_mealsite)
    
    if mealsite is None or (mealsite != new_mealsite and new_mealsite is not None): 
        set_new_mealsite = True
        mealsite = new_mealsite
    

    races = []
    for race in database_constants.RACE_OPTIONS:
        races.append(request.args.get(race))
    races = list(filter(None, races))
    racecsv = ",".join(races)
        
    language = request.args.get('language')
    age_range = request.args.get('age_range')
    gender = request.args.get('gender')
    zip_code = request.args.get('zip_codes')
    homeless = request.args.get('homeless')
    veteran = request.args.get('veteran')
    disabled = request.args.get('disabled')
    guessed = request.args.get('patron_response')

    patron_data = {"race": racecsv, "language": language,
    "age_range": age_range, "gender": gender, "zip_code": zip_code, 
    "homeless": homeless, "veteran": veteran, "disabled": disabled,
    "guessed": guessed}

    print(patron_data)
    
    if (any(patron_data.values()) and patron_data["guessed"]):
        patron_data["meal_site"] = mealsite
        demographic_db.add_patron(patron_data)
        html_code = render_template('submitpatrondata.html',
        ampm=get_ampm(),
        current_time=get_current_time(),
        otherlanguages = database_constants.otherlanguages,
        races = database_constants.races,
        ages = database_constants.ages,
        genders = database_constants.genders,
        zip_codes = database_constants.ZIP_CODE_OPTIONS,
        homeless_options = database_constants.HOMELESS_OPTIONS,
        veteran_options = database_constants.VETERAN_OPTIONS,
        disabled_options = database_constants.DISABLED_OPTIONS,
        patron_response_options = database_constants.GUESSED_OPTIONS
        )
        response = make_response(html_code)

        if set_new_mealsite:
            response.set_cookie('site', mealsite)

        return response
    else:
        html_code = '<p color = red> "Invalid Syntax"<\p>'
        response = make_response(html_code)
    

 #-----------------------------------------------------------------------


@app.route('/admin', methods=['GET'])
@login_required(must=[be_admin])
def admindisplaydata():
    
    return render_template(
        "admin.html"
    )


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