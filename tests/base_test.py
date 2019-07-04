"""
Base Test case with setup and methods that other
test classes inherit
"""
import os
import unittest
import json
import datetime

from app import create_app, db
from manage import create_admin


class BaseTestCase(unittest.TestCase):
    """Base Test Case"""
    def setUp(self):
        """Set up test variables"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            create_admin()
        self.data = {}
        self.header = {'Content-Type': 'application/json'}
        self.reg_data = {
            "name": "stephen",
            "email": "user@test.com",
            "password": "Tests12!@"
        }
        self.admin_data = {
            "email": os.getenv('ADMIN_EMAIL'),
            "password": os.getenv('ADMIN_PASSWORD')
        }
        self.airport_data = {
            "name": "JKIA",
            "country": "Kenya",
            "city": "Nairobi"
        }
        self.airplane_data = {
            "reg_number": "FKJL76T",
            "economy_seats": 50,
            "business_seats": 10,
            "first_class_seats": 5
        }
        self.flight_data = {
            "departure_date": "Jul 06 2019 12:00PM",
            "departure_airport_id": 1,
            "arrival_date": "Jul 06 2019 11:00PM",
            "arrival_airport_id": 2,
            "airplane_id": 1
        }
        self.arrival_airport_data = {
            "name": "KISUMU",
            "country": "Kenya",
            "city": "Kisumu"
        }
        self.booking_data = {
            "name": "KISUMU",
            "country": "Kenya",
            "city": "Kisumu"
        }

    def login(self):
        "login a test user"
        self.client.post('/api/register', headers=self.header,
                         data=json.dumps(self.reg_data))
        return self.client.post('/api/login', headers=self.header,
                                data=json.dumps(self.reg_data))

    def get_login_token(self):
        """Get the access token and add it to the header"""
        login_res = self.login()
        result = json.loads(login_res.data.decode())
        self.header['Authorization'] = 'Bearer ' + result['access_token']
        return result

    def admin_login(self):
        "login admin test user"
        login_res = self.client.post('/api/login', headers=self.header,
                                     data=json.dumps(self.admin_data))
        result = json.loads(login_res.data.decode())
        self.header['Authorization'] = 'Bearer ' + result['access_token']

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()