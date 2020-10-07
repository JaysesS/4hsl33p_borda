from flask import Flask

from .models import db
from . import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['DEBUG'] = False
app.config['SECRET_KEY'] = '***'
app.config['APPLICATION_ROOT'] = '/'
app.config['WTF_CSRF_ENABLED'] = False
app.config['WTF_CSRF_METHODS'] = []

app.app_context().push()
db.init_app(app)
db.create_all()

from .views import *