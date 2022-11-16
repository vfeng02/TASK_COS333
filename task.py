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
from TASKdbcode import tabledashboard
from TASKdbcode import piedashboard
from TASKdbcode import bardashboard
from TASKdbcode import linedashboard

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
        app = tabledashboard.init_tabledashboard(app)
        app = piedashboard.init_piedashboard(app)
        app = bardashboard.init_bardashboard(app)
        app = linedashboard.init_linedashboard(app)

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
@app.route('/about', methods=['GET'])
@login_required(basic=True)
def selectmealsit1e():

    html_code = render_template('about.html')
    response = make_response(html_code)
    return response
 #-----------------------------------------------------------------------

@app.route('/submitpatrondata', methods=['GET'])
#@login_required(basic=True)
def submitpatrondata():
    # mealsite = request.args.get('mealsite')
    new_mealsite = request.args.get('mealsite')
    mealsite = request.cookies.get('site')
    set_new_mealsite = False         
    print("selected site")
    print(mealsite)
    if mealsite is None or (mealsite != new_mealsite and new_mealsite is not None): 
        set_new_mealsite = True
        mealsite = new_mealsite

    races = []
    for race in database_constants.RACE_OPTIONS:
        races.append(request.args.get(race))
    races = list(filter(None, races))
    racecsv = ",".join(races)
        
    language = request.args.get('language')
    print('language',language)
    age_range = request.args.get('age_range')
    # problem because the names changed
    gender = request.args.get('gender')
    zip_code = request.args.get('zip_codes')
    homeless = request.args.get('homeless')
    veteran = request.args.get('veteran')
    disabled = request.args.get('disabled')
    guessed = request.args.get('guessed')
    print('guess',guessed)

    patron_data = {"race": racecsv, "language": language,
    "age_range": age_range, "gender": gender, "zip_code": zip_code, 
    "homeless": homeless, "veteran": veteran, "disabled": disabled,
    "guessed": guessed}

    # print(patron_data)

    # print(any(patron_data.values()))
    
    if (any(patron_data.values())):
            patron_data["meal_site"] = mealsite
            demographic_db.add_patron(patron_data)

    html_code = render_template('submitpatrondata.html',
        mealsite = mealsite,
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
        patron_response_options = database_constants.GUESSED_OPTIONS,
        racecheck = ""
        )
    response = make_response(html_code)

    if set_new_mealsite:
        response.set_cookie('site', mealsite)

    return response

 #-----------------------------------------------------------------------


@app.route('/admin', methods=['GET'])
# @login_required(must=[be_admin])
def admindisplaydata():
    return render_template(
        "admin.html"
    )

@app.route('/register', methods=['GET'])
#@login_required(must=[be_admin])
def register(): 

    return render_template(
        "register.html"
    )

@app.route('/deletelastpatron')
#@login_required(basic=True)
def deletelast():
    meal_site = request.args.get('mealsite')
    demographic_db.delete_last_patron(meal_site)
    html_code = render_template('submitpatrondata.html',
        mealsite = meal_site,
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
        patron_response_options = database_constants.GUESSED_OPTIONS,
        racecheck = ""
        )
    response = make_response(html_code)
    return response

@app.route('/getlastpatron')
#@login_required(basic=True)
def getlast():
    meal_site = request.args.get('mealsite')
    last = demographic_db.get_last_patron(meal_site)
    print(last['meal_site'])
    html_code = render_template('submitpatrondata.html',
        mealsite = meal_site,
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
        patron_response_options = database_constants.GUESSED_OPTIONS,
        lastrace = last['race'],
        lastlanguage = last['language'],
        lastage = last['age_range'],
        lastgender = last['gender'],
        lastzip = last['zip_code'],
        lasthomeless = last['homeless'],
        lastveteran = last['veteran'],
        lastdisabled = last['disabled'],
        lastguess = last['guessed']
        )
    response = make_response(html_code)
    return response
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



