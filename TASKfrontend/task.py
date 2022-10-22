import time
import flask
import sys
# from demographic_db import add_patron
# import os
# import urllib.parse as up
# import psycopg2
# import contextlib
# import demographic_db

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='templates')
# sys.path.insert(0, '../TASKdbcode')
# sys.path.insert(0, '/Users/vicky/Desktop/COS333/TASK_COS333/Taskdbcode')
# DATABASE_URL = 'postgres://usqmchwx:jVw_QrUQ-blJpl1dXhixIQmPAsD89W-R@peanut.db.elephantsql.com/usqmchwx'

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
    html_code = flask.render_template('index.html',
    ampm=get_ampm(),
    current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

 #-----------------------------------------------------------------------

@app.route('/submitpatrondata', methods=['GET'])
def submitpatrondata():
    language = flask.request.cookies.get('language')
    print(language)

    html_code = flask.render_template('submitpatrondata.html',
    ampm=get_ampm(),
    current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

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