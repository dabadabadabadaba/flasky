from flask import Flask
from flask_sqlalchemy import SQLAlchemy #have to import SQLAlchemy
from flask_migrate import Migrate

#setting up the database, setting up initial objects for us to use later in our app
database = SQLAlchemy()
migrate = Migrate() 


def create_app():
    # __name__ stores the name of the module we're in. 
    # Flask is doing something with it under the hood and we don't really have to worry about why.
    app = Flask(__name__)
    
    #configuration variables
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # telling app where the database lives:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/breakfasts_development'

    #connect database to app:
    database.init_app(app)
    migrate.init_app(app, database)

    # import the model
    from app.models.breakfast import Breakfast

# import inside the body of the function bc that's how it's done in Flask
    from .routes.breakfast import breakfast_bp
    app.register_blueprint(breakfast_bp)

    return app