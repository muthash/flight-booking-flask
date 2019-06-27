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
        self.assertEqual(result['message'], "Account created successfully, " +
                         "A confirmation email has been sent.")
        self.assertEqual(res.status_code, 201)


        # def test_registration(self):
        # """Test user registration works correcty."""
        # res = self.client().post('/auth/register', data=self.user_data)
        # # get the results returned in json format
        # result = json.loads(res.data.decode())
        # # assert that the request contains a success message and a 201 status code
        # self.assertEqual(result['message'], "You registered successfully.")
        # self.assertEqual(res.status_code, 201)

