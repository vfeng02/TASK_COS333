#!/usr/bin/env python

#-----------------------------------------------------------------------
# task.py
# Author: Vicky Feng and Andres Blanco Bonilla
# Runs simple HTML form to input data into the TASK demographic database
#-----------------------------------------------------------------------

from ctypes import set_errno
from dis import dis
import time
from flask import Flask, request, session, jsonify
from flask import render_template, make_response
# sys.path.insert(0, 'TASKdbcode')
# sys.path.insert(0, 'TASKfrontend/templates')
from TASKdbcode import database_constants
from TASKdbcode import demographic_db
from TASKdbcode import tabledashboard
from TASKdbcode import piedashboard
from TASKdbcode import bardashboard
from TASKdbcode import linedashboard
from TASKdbcode import counttabledashboard
import sqlalchemy
import sys
from werkzeug.security import generate_password_hash,\
    check_password_hash

# from database_constants import mealsites, languages, races, ages, genders, zip_codes
# from database_constants import HOMELESS_OPTIONS
import psycopg2
from flask_simplelogin import SimpleLogin, get_username, login_required, is_logged_in
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user
#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates', instance_relative_config=False)

csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')
# login_manager = LoginManager()
# login_manager.login_view = 'login'
with app.app_context():
        app = tabledashboard.init_tabledashboard(app)
        app = piedashboard.init_piedashboard(app)
        app = bardashboard.init_bardashboard(app)
        app = linedashboard.init_linedashboard(app)
        app = counttabledashboard.init_counttabledashboard(app)
        csrf.init_app(app)
        app.config["SECRET_KEY"] = "andresallisonvickyrohan"
        app.secret_key = "andresallisonvickyrohan"
        #login_manager.init_app(app)
        SimpleLogin(app, login_checker=demographic_db.check_my_users)

#-----------------------------------------------------------------------

def be_admin(username):
    if username == "jaimeparker":
        return True
    else: 
        return False

# @login_manager.user_loader
# def load_user(user_id):
#     return demographic_db.user_exists(user_id)

def get_ampm():
    if time.strftime('%p') == "AM":
        return 'morning'
    return 'afternoon'

def get_current_time():
    return time.asctime(time.localtime())

 #-----------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login(): 
    # admin = demographic_db.be_admin(get_username)
    # # session["admin"] = admin
    # login.set_cookie('admin', admin)

    # user = {'username': request.args.get("username"), "password":request.args.get('password')}

    # check = demographic_db.check_my_users(user)
    # if check: 
    #     login_user()

    check = demographic_db.be_admin(request.args.get("username"))
    login = make_response(render_template("login.html"))
    login.set_cookie('admin', check)
    return login

def admin_cookies(): 
    admin = request.get_cookie('admin')
    if admin is True: 
        return True
    return False

# @app.route('/logout', methods=['POST'])
# def logout():
#     logout_user()
#     return redirect("/login")

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
@login_required(basic=True)
def submitpatrondata():
    # mealsite = request.args.get('mealsite')
    new_mealsite = request.args.get('mealsite')
    mealsite = request.cookies.get('site')
    set_new_mealsite = False         
    # print("selected site")
    # print(mealsite)
    if mealsite is None or (mealsite != new_mealsite and new_mealsite is not None): 
        set_new_mealsite = True
        mealsite = new_mealsite

    races = []
    # print(request.args.getlist('race'))
    if request.args.getlist('race') is not None:
        for race in request.args.getlist('race'):
            races.append(race)
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
    # print('guess',guessed)

    patron_data = {"race": racecsv, "language": language,
    "age_range": age_range, "gender": gender, "zip_code": zip_code, 
    "homeless": homeless, "veteran": veteran, "disabled": disabled,
    "guessed": guessed}

    # print(patron_data)

    # print(any(patron_data.values()))

    zip_codes_by_mealsite = database_constants.ZIP_CODES[database_constants.MEAL_SITE_LOCATIONS[mealsite]]
    
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
        zip_codes = zip_codes_by_mealsite,
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
@login_required(must=[admin_cookies])
def admindisplaydata():
    return render_template(
        "admin.html"
    )

# @app.route("/lineapp/", methods=['POST','GET'])
# @login_required(must=[demographic_db.be_admin])
# def lineapp():
#     return line_app.index()

# @app.route("/barapp/", methods=['POST','GET'])
# @login_required(must=[demographic_db.be_admin])
# def barapp():
#     return bar_app.index()

# @app.route("/pieapp/", methods=['POST','GET'])
# @login_required(must=[demographic_db.be_admin])
# def pieapp():
#     return pie_app.index()

# @app.route("/tableapp/", methods=['POST','GET'])
# @login_required(must=[demographic_db.be_admin])
# def tableapp():
#     return table_app.index()


# --------------------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
@login_required(must=[demographic_db.be_admin])
def register(): 
    email = request.args.get('email')
    password = request.args.get('password')
    account_type = request.args.get('AccountType')
    repeat_password = request.args.get('repeatPassword')
    if password != repeat_password: 
        print("Passwords do not match")
    account_details = {"username": email, "email": email, "password": password, "role": account_type}
    demographic_db.add_user(account_details)

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



