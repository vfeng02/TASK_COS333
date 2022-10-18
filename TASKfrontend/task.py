import time
import flask
import demographic_db

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='templates')

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

@app.route('/form', methods=['GET'])
def form():
    prev_name = flask.request.cookies.get('prev_name')
    if prev_name is None:
        prev_name = '(None)'

    html_code = flask.render_template('form.html',
    ampm=get_ampm(),
    current_time=get_current_time(),
    prev_name=prev_name)
    response = flask.make_response(html_code)
    return response

 #-----------------------------------------------------------------------

@app.route('/submitresult', methods=['GET'])
def submit_result():
    name = flask.request.args.get('name')
    if name is None:
        name = ''
        name = name.strip()

    if name == '':
        prev_name = '(None)'
    else:
        prev_name = name
        # submit name to the db
        # books = demographic_db.get_books(author) # Exception handling omitted

    html_code = flask.render_template('submitresult.html',
        ampm=get_ampm(),
        current_time=get_current_time(),
        name=prev_name)
    response = flask.make_response(html_code)
    response.set_cookie('prev_name', prev_name)
    return response