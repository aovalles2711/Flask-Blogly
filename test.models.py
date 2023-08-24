from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Test for model for Users."""

    def setUp(self):
        """Remove any existing users."""

        User.query.delete()
    
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_greet(self):
        user = User(name="TestUser")
        self.assertEquals(user.greet(), "I'm TestUser a user.")

    def test_get_by_last_name(self):
        user = User(first_name="JohnnyTest", last_name="AppleseedTest")
        db.session.add(user)
        db.session.commit()

        last_names = User.get_by_last_name('AppleseedTest')
        self.assertEquals(last_names, [user])