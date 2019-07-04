"""Test case for the user functionality"""
import os
import json

from io import BytesIO

from tests.base_test import BaseTestCase


class TestRegisterUser(BaseTestCase):
    """Test for Register User endpoint"""
    def register(self):
        return self.client.post('/api/register', headers=self.header,
                                data=json.dumps(self.reg_data))

    def test_registration(self):
        """Test user registration works correcty"""
        res = self.register()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Account created successfully")
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice"""
        self.register()
        res = self.register()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "User already exists, Please login")
        self.assertEqual(res.status_code, 409)

    def test_register_safe_username(self):
        """Test user registration with reserved names"""
        self.reg_data['name'] = "login"
        res = self.register()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "The name you provided is not allowed, " +
                         "please try again but with a different name.")
        self.assertEqual(res.status_code, 400)

    def test_invalid_password_pattern(self):
        """Test register with short password length"""
        self.reg_data['password'] = 'password'
        res = self.register()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Password should contain at least eight characters " +
                         "with at least one digit, one uppercase letter and " +
                         "one lowercase letter.")
        self.assertEqual(res.status_code, 400)

    def test_register_invalid_email(self):
        """Test user registration with a non deliverable email address"""
        self.reg_data['email'] = 'invalid@asbvggghv.ck'
        res = self.register()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "The domain name asbvggghv.ck does not exist.")
        self.assertEqual(res.status_code, 400)


class TestLoginUser(BaseTestCase):
    """Test for Login User endpoint"""
    def test_user_login(self):
        """Test registered user can login"""
        res = self.login()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Login successfull")
        self.assertTrue(result['access_token'])
        self.assertEqual(res.status_code, 200)

    def test_login_invalid_email(self):
        """Test user login with invalid email"""
        self.login()
        self.reg_data['email'] = "invalid@email.com"
        res = self.client.post('/api/login', headers=self.header,
                               data=json.dumps(self.reg_data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Invalid email or password Please try again")
        self.assertEqual(res.status_code, 401)


class TestPassportUpload(BaseTestCase):
    """Test for upload passport User endpoint"""
    def uploadpassport(self):
        self.data['passport_image'] = (BytesIO(b"abcdef"), 'test.jpg')
        self.get_login_token()
        return self.client.put('api/uploads/passport',
                               headers=self.header,
                               content_type='multipart/form-data',
                               data=self.data)

    def test_file_upload(self):
        """Test image upload works as expected"""
        res = self.uploadpassport()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "File uploaded successfully")
        self.assertEqual(res.status_code, 201)

    def test_file_update(self):
        """Test image update works as expected"""
        self.uploadpassport()
        res = self.uploadpassport()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "File uploaded successfully")
        self.assertEqual(res.status_code, 201)

    def test_delete_file(self):
        """Test delete image works as expected"""
        self.uploadpassport()
        res = self.client.delete('api/uploads/passport',
                                 headers=self.header)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "File deleted successfully")
        self.assertEqual(res.status_code, 200)

    def test_delete_no_file(self):
        """Test delete empty image file not allowed"""
        self.get_login_token()
        res = self.client.delete('api/uploads/passport',
                                 headers=self.header)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Cannot delete blank image file")
        self.assertEqual(res.status_code, 401)
