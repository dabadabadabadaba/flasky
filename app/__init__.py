from flask import Flask
from flask_sqlalchemy import SQLAlchemy #have to import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv # allows us to load variables from dotenv environment (our .env file)
import os #allows us to pull things out of our environment

#setting up the database, setting up initial objects for us to use later in our app
database = SQLAlchemy()
migrate = Migrate()
load_dotenv() # this calls variables from .env


def create_app(testing = None): # "testing = None" will allow us to set up our app in a testing format
    # __name__ stores the name of the module we're in. 
    # Flask is doing something with it under the hood and we don't really have to worry about why.
    app = Flask(__name__)
    
    #configuration variables:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #will show SQLAlchemy under the hood:
    app.config['SQLALCHEMY_ECHO'] = True
    
    if testing is None:
        #telling app where the database lives:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') # grabbing the variable out of the .env, this one IS in quotes
    else:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_SQLALCHEMY_DATABASE_URI')

    #connect database to app:
    database.init_app(app)
    migrate.init_app(app, database)

    #imports the model Breakfast into the project so migrations can pick it up and add to database
    from app.models.breakfast import Breakfast

    #import inside the body of the function bc that's how it's done in Flask
    from .routes.breakfast import breakfast_bp
    app.register_blueprint(breakfast_bp)

    return app