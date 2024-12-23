import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.planets import Planet

# Wave 6
load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }

    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_planets(app):
    planet_1 = Planet(name="Mercury", description="Smallest, closest to the Sun, extreme temperatures.", distance_from_sun=57.9)
    planet_2 = Planet(name="Venus", description="Hot, toxic atmosphere, Earth's size, rotates backward.", distance_from_sun=108.2)

    db.session.add_all([planet_1,planet_2])

    db.session.commit()
