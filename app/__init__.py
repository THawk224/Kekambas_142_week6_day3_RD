from flask import Flask # Import the Flask class from the flask module
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config # Import the Config class from the config module

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

# Create an instance of SQLAlchemy called db which will be used to create the database
db = SQLAlchemy(app)
# Create an instance of Migrate called migrate which will be used to create the migrations
migrate = Migrate(app, db)

# Import the routes to the application and also the models 
from . import models, routes 