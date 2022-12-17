#!/usr/bin/env python

#-----------------------------------------------------------------------
# task.py
# Author: Vicky Feng and Andres Blanco Bonilla and Rohan Amin
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
from TASKdbcode import counttabledashboard
from pretty_html_table import build_table
import sqlalchemy
import sys
import textwrap
from werkzeug.security import generate_password_hash,\
    check_password_hash

# from database_constants import mealsites, languages, races, ages, genders, zip_codes
# from database_constants import HOMELESS_OPTIONS
import psycopg2
from flask_simplelogin import SimpleLogin, get_username, login_required, is_logged_in
from flask_wtf.csrf import CSRFProtect
#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')
csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')
with app.app_context():
        app = tabledashboard.init_tabledashboard(app)
        app = piedashboard.init_piedashboard(app)
        app = bardashboard.init_bardashboard(app)
        app = linedashboard.init_linedashboard(app)
        app = counttabledashboard.init_counttabledashboard(app)
        csrf.init_app(app)

        app.config["SECRET_KEY"] = "andresallisonvickyrohan"

        SimpleLogin(app, login_checker=demographic_db.check_my_users)

#-----------------------------------------------------------------------


def get_ampm():
    if time.strftime('%p') == "AM":
        return 'morning'
    return 'afternoon'

def get_current_time():
    return time.asctime(time.localtime())

 #-----------------------------------------------------------------------
@app.route('/login', methods=['GET','POST'])
def login(): 
    
    return render_template("login.html")


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
def selectmealsit1e():

    html_code = render_template('about.html')
    response = make_response(html_code)
    return response
 #-----------------------------------------------------------------------

@app.route('/submitpatrondata', methods=['GET','POST'])
@login_required(basic=True)
def submitpatrondata():
    new_mealsite = request.args.get('mealsite')
    mealsite = request.cookies.get('mealsite')
    new = False
    num = request.cookies.get('num')
    if mealsite is None or (mealsite != new_mealsite and new_mealsite is not None): 
        new = True
        mealsite = new_mealsite
        num = '0'
    
    submitted = request.form.get('language')
    if submitted:
        num = str(int(num)+1)   
    

    races = []
    if request.form.getlist('race') is not None:
        for race in request.form.getlist('race'):
            if (race != 'Unknown'):
                if race == "Native":
                    races.append("Native Hawaiian/Pacific Islander")
                elif race == "American":
                    races.append("American Indian/Alaska Native")
                else:
                    races.append(race)
        races = list(filter(None, races))
    print("RACE", races)
    racecsv = ",".join(races)
    language = request.form.get('language')
    age_range = request.form.get('age_range')
    # problem because the names changed
    gender = request.form.get('gender')
    zip_code = request.form.get('zip_codes')
    homeless = request.form.get('homeless')
    veteran = request.form.get('veteran')
    disabled = request.form.get('disabled')
    guessed = request.form.get('guessed')
    # print('guess',guessed)

    patron_data = {"race": racecsv, "language": language,
    "age_range": age_range, "gender": gender, "zip_code": zip_code, 
    "homeless": homeless, "veteran": veteran, "disabled": disabled,
    "guessed": guessed}


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
        ages = database_constants.AGE_RANGE_OPTIONS,
        genders = database_constants.genders,
        zip_codes = zip_codes_by_mealsite,
        homeless_options = database_constants.HOMELESS_OPTIONS,
        veteran_options = database_constants.VETERAN_OPTIONS,
        disabled_options = database_constants.DISABLED_OPTIONS,
        patron_response_options = database_constants.GUESSED_OPTIONS,
        num = num,
        )
    response = make_response(html_code)
    response.set_cookie('num',num)
    if new:
        response.set_cookie('mealsite', new_mealsite)
   
    return response

 #-----------------------------------------------------------------------


@app.route('/admin', methods=['GET'])
@login_required(must=[demographic_db.be_admin])
def admindisplaydata():
    return render_template(
        "admin.html"
    )



@app.route('/register', methods=['GET', 'POST'])
@login_required(must=[demographic_db.be_admin])
def register(): 
    success = ''
    username = request.form.get('username')
    if username:
        password = request.form.get('password')
        account_type = 'representative'
        repeat_password = request.form.get('repeatPassword')
        if password != repeat_password: 
            success = "Error: Passwords do not match"
        else: 
            account_details = {"username": username, "password": password, "role": account_type}
            result = demographic_db.add_user(account_details)
            if result:
                success = "Success! Registered "+username+" as a TASK representative."
            else:
                success = "Error: Username taken, please try another."
    return render_template(
        "register.html", success = success
    )

@app.route('/users', methods=['GET','POST'])
@login_required(must=[demographic_db.be_admin])
def viewusers(): 
    return render_template("userdashboard.html")

@app.route('/viewusers', methods=['GET','POST'])
@login_required(must=[demographic_db.be_admin])
def users(): 
    df = demographic_db.get_users()
    html = build_table(df, 'blue_light', padding='20px', even_color = 'black')
    return render_template("viewusers.html",table=html, titles=df.columns.values, success = '')

@app.route('/deleteusers', methods=['GET','POST'])
@login_required(must=[demographic_db.be_admin])
def deleteuser(): 
    success = ''
    username = request.form.get('user')
    print(username)
    if username:
        if username == "jaimeparker":
            success = 'You may not delete the administrator credentials from the system.'
        else:
            result = demographic_db.delete_user(username)
            if not result:
                success = 'User does not exist in system, please try again.'
    df = demographic_db.get_users()
    html = build_table(df, 'blue_light', padding='20px', even_color = 'black')
    return render_template("deleteusers.html",table=html, titles=df.columns.values, role = 'All', success = success)


@app.route('/deletelastpatron')
@login_required(basic=True)
def deletelast():
    meal_site = request.args.get('mealsite')
    num = request.cookies.get('num')
    if int(num) >0:
        num = str(int(num) -1)
        demographic_db.delete_last_patron(meal_site)
    else:
        num = '0'
 
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
        num = num
        )
    response = make_response(html_code)
    response.set_cookie('num', num)
    return response

@app.route('/getlastpatron')
@login_required(basic=True)
def getlast():
    meal_site = request.args.get('mealsite')
    last = demographic_db.get_last_patron(meal_site)
    lastrace = last['race'].iloc[0]
    print(lastrace)
    lastrace = "\n".join(textwrap.wrap(lastrace, width=20))
    html_code = render_template('prev.html',
        lastrace = lastrace,
        lastlanguage = last['language'].iloc[0],
        lastage = last['age_range'].iloc[0],
        lastgender = last['gender'].iloc[0],
        lastzip = last['zip_code'].iloc[0],
        lasthomeless = last['homeless'].iloc[0],
        lastveteran = last['veteran'].iloc[0],
        lastdisabled = last['disabled'].iloc[0],
        lastguess = last['guessed'].iloc[0],
        last = last
        )
    response = make_response(html_code)
    return response
    