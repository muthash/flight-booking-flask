"""
Base Test case with setup and methods that other
test classes inherit
"""
import unittest
import json
import datetime
from app import create_app, db


class BaseTestCase(unittest.TestCase):
    """Base Test Case"""
    def setUp(self):
        """Set up test variables"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.header = {'Content-Type': 'application/json'}
        self.reg_data = {"name": "stephen",
                         "email": "user@test.com",
                         "password": "Tests12!@"}



        # self.reg_data = {'email': 'user@test.com', 'name': 'stephen',
        #                  'password': 'Tests12!@'}

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()