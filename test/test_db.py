import unittest
from flask_bcrypt import Bcrypt
from tools.config import TestConfig
from tools.extensions import db
from app import create_app
from models import User


class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        testApp = create_app(TestConfig)
        self.encryption_alg = Bcrypt(testApp)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
        self.add_test_data_to_db()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_user(self):
        """
        Tests if the database is properly configured to get users
        """
        alex = User.query.filter(User.username == "Alex").first()
        self.assertIsNotNone(alex)
        blex = User.query.filter(User.username == "Blex").first()
        self.assertIsNone(blex)

    def test_password_hashing(self):
        alex = User.query.filter(User.username == "Alex").first()
        self.assertTrue(self.encryption_alg.check_password_hash(alex.password_hash, "epic"))

    def add_test_data_to_db(self):
        new_user = User(username="Alex", password_hash=self.encryption_alg.generate_password_hash("epic"))  # type: ignore
        db.session.add(new_user)
        db.session.commit()
