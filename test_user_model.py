"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(u.__repr__(),f"<User #{u.id}: {u.username}, {u.email}>")

    def test_user_follow_methods(self):
        """Does following logic work?"""

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        u1.following.append(u2)

        db.session.add(u1,u2)
        db.session.commit()


        self.assertTrue(u1.is_following(u2))
        self.assertTrue(u2.is_followed_by(u1))

        u1.following.remove(u2)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u2.is_followed_by(u1))


    def test_user_creation_methods(self):
        """Does creating user work?"""

        u = User.signup("testuser","test@test.com","secret123", User.image_url.default.arg)
        self.assertIsInstance(u,User)
        self.assertRaises(TypeError,User.signup,"testuser","secret123", User.image_url.default.arg)
    

    def test_user_authentication(self):
        """Does authenticatig user work?"""
        User.signup("kidist","test@test.com","myPass123", User.image_url.default.arg)
        u = User.authenticate("kidist","myPass123")
        self.assertIsInstance(u,User)
        self.assertFalse(User.authenticate("kidist","myPass12"))
        self.assertFalse(User.authenticate("kidis","myPass123"))

