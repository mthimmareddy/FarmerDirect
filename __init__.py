from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
from flask import session
#from flask.ext.googlemaps import GoogleMaps



######### Enable this for debugging #########
# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# SQLALCHEMY_TRACK_MODIFICATIONS = True
######## Enable this for debugging #########

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myscecretkey12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://servinglocalindi:manju123@servinglocalindia.mysql.pythonanywhere-services.com/servinglocalindi$l1'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


#maps = GoogleMaps(app)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

######### Required in Case of firing complex queries without ORM #########
#db2 = yaml.load(open('config.yaml'))
app.config['MYSQL_HOST'] = 'servinglocalindia.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'servinglocalindi'

app.config['MYSQL_PASSWORD'] = 'manju123'
app.config['MYSQL_DB'] = 'servinglocalindi$l1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
######### Required in Case of firing complex queries without ORM #########


# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
#
import models
import routes
models.db.create_all()



