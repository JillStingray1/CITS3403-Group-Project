from selenium import webdriver
from flask import render_template
import unittest
from app import create_app
from tools.config import TestConfig
from tools.extensions import db
from routes import user_routes, meeting_routes
import multiprocessing
from flask_bcrypt import Bcrypt

local_host = "http://localhost:5000/"


class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()

        # adds the routes to test app
        @self.testApp.route("/")
        def index():
            return render_template("index.html")

        user_routes.init_user_routes(self.testApp, db, Bcrypt(self.testApp))
        meeting_routes.init_meeting_routes(self.testApp, db)

        self.server_thread = multiprocessing.Process(target=self.testApp.run)
        self.server_thread.start()

        self.driver = webdriver.Firefox()
        self.driver.get(local_host)
        self.driver.implicitly_wait(10)

    def test_signup(self):
        """
        Attempts to sign in with a new account, and checks success on whether
        we reach the main menu
        """
        # find the sign up button on the index page and click
        self.driver.find_element(value="signup").click()

        # get the form fields
        username_field = self.driver.find_element(value="username")
        password_field = self.driver.find_element(value="password")
        confirm_field = self.driver.find_element(value="confirmPassword")

        # fill in user details and submit
        username_field.send_keys("Joel3")
        password_field.send_keys("Apple")
        confirm_field.send_keys("Apple")
        self.driver.find_element(value="submit").click()

        # check if we get to the main menu
        self.assertEqual(self.driver.current_url, local_host + "main-menu")

    def test_auto_login(self):
        """
        Tests the functionality of automatically logging users that
        are not logged out
        """
        # sign up to make user session
        self.driver.find_element(value="signup").click()
        username_field = self.driver.find_element(value="username")
        password_field = self.driver.find_element(value="password")
        confirm_field = self.driver.find_element(value="confirmPassword")
        username_field.send_keys("Joel3")
        password_field.send_keys("Apple")
        confirm_field.send_keys("Apple")
        self.driver.find_element(value="submit").click()

        self.driver.get(local_host)
        self.driver.find_element(value="login").click()
        self.assertEqual(self.driver.current_url, local_host + "main-menu")

    def test_logout(self):
        """
        Tests logging out, auto login should be disabled if you press log
        out on the main menu
        """
        # sign up to make user session
        self.driver.find_element(value="signup").click()
        username_field = self.driver.find_element(value="username")
        password_field = self.driver.find_element(value="password")
        confirm_field = self.driver.find_element(value="confirmPassword")
        username_field.send_keys("Joel3")
        password_field.send_keys("Apple")
        confirm_field.send_keys("Apple")
        self.driver.find_element(value="submit").click()
        self.driver.find_element(value="logout").click()
        self.driver.find_element(value="login").click()
        self.assertEqual(self.driver.current_url, local_host + "user/login")

    def tearDown(self) -> None:
        self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
