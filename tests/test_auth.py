"""Test case for the user functionality"""
import json

from tests.base_test import BaseTestCase


class TestRegisterUser(BaseTestCase):
    """Test for Register User endpoint"""
    def test_registration(self):
        """Test user registration works correcty"""
        res = self.client.post('/api/register', headers=self.header,
                               data=json.dumps(self.reg_data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Account created successfully")
        self.assertEqual(res.status_code, 201)


class TestLoginUser(BaseTestCase):
    """Test for Login User endpoint"""

    def test_user_login(self):
        """Test registered user can login."""
        self.client.post('/api/register', headers=self.header,
                         data=json.dumps(self.reg_data))
        res = self.client.post('/api/login', headers=self.header,
                               data=json.dumps(self.reg_data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Login successfull")
        self.assertTrue(result['access_token'])
        self.assertEqual(res.status_code, 200)
