import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.breakfast import Breakfast

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra): # if the request is finished, we're not using the database anymore, **extra means any extra variables that might be passed in 
        db.session.remove
    
    with app.app_context():
        db.create_all()
        yield app
    
    with app.app_context(): 
        db.drop_all()

@pytest.fixture
def client(app): # the app that's passed in is referring the fixture above
    return app.test_client()

@pytest.fixture
def two_breakfasts(app):
    breakfast1 = Breakfast(name="doughnut", rating=5.0, prep_time=1)
    breakfast2 = Breakfast(name="tea", rating=4.0, prep_time=5)

    db.session.add(breakfast1)
    db.session.add(breakfast2)
    db.session.commit()
