from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import dotenv_values

app = Flask(__name__)
config = dotenv_values('.env')
app.config['SECRET_KEY'] = config.get('SECRET_KEY')
# app.config['JWT_COOKIE_SECURE'] = False
# app.config['JWT_TOKEN_LOCATION'] = ['cookies']
# app.config['JWT_COOKIE_CSRF_PROTECT'] = False
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=3)
# app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost/hr_mgmt'
bcrypt = Bcrypt(app)
db = SQLAlchemy()
db.init_app(app)
jwt = JWTManager(app)
CORS(app)


from flask_app import index
