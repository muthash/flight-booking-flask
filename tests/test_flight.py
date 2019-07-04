"""Test case for the flight creation functionality"""
import os
import json

from tests.base_test import BaseTestCase


class TestAirportManipulation(BaseTestCase):
    """Test for Airport manipulation endpoint"""
    def test_admin_airport_addition(self):
        """Test adding airport by admin works correcty"""
        self.admin_login()
        res = self.client.post('api/airport',
                               headers=self.header,
                               data=json.dumps(self.airport_data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Airport registered successfully")
        self.assertEqual(res.status_code, 201)

    def test_user_airport_addition(self):
        """Test adding airport by user is not possible"""
        self.get_login_token()
        res = self.client.post('api/airport',
                               headers=self.header,
                               data=json.dumps(self.airport_data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Forbidden, Admins only!")
        self.assertEqual(res.status_code, 403)

    def test_get_available_airports(self):
        """Test get all available airports"""
        self.admin_login()
        self.client.post('api/airport',
                         headers=self.header,
                         data=json.dumps(self.airport_data))
        res = self.client.get('api/airport',
                              headers=self.header)
        result = json.loads(res.data.decode())
        self.assertEqual(result['number_of_airports'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_no_airports(self):
        """Test get all airports before adding"""
        self.admin_login()
        res = self.client.get('api/airport',
                              headers=self.header)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "No data to display")
        self.assertEqual(res.status_code, 200)


class TestAirplaneManipulation(BaseTestCase):
    """Test for Airplane manipulation endpoint"""
    def test_admin_airport_addition(self):
        """Test adding airplane by admin works correcty"""
        self.admin_login()
        res = self.client.post('api/airplane',
                               headers=self.header,
                               data=json.dumps(self.airplane_data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Airplane registered successfully")
        self.assertEqual(res.status_code, 201)

    def test_user_airplane_addition(self):
        """Test adding airplane by user is not possible"""
        self.get_login_token()
        res = self.client.post('api/airplane',
                               headers=self.header,
                               data=json.dumps(self.airplane_data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Forbidden, Admins only!")
        self.assertEqual(res.status_code, 403)

    def test_get_available_airplanes(self):
        """Test get all available airplanes"""
        self.admin_login()
        self.client.post('api/airplane',
                         headers=self.header,
                         data=json.dumps(self.airplane_data))
        res = self.client.get('api/airplane',
                              headers=self.header)
        result = json.loads(res.data.decode())
        self.assertEqual(result['number_of_airplanes'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_no_airplanes(self):
        """Test get all airplanes before adding"""
        self.admin_login()
        res = self.client.get('api/airplane',
                              headers=self.header)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "No data to display")
        self.assertEqual(res.status_code, 200)


class TestFlightManipulation(BaseTestCase):
    """Test for Flight manipulation endpoint"""
    def create_flight(self):
        self.admin_login()
        self.client.post('api/airport',
                         headers=self.header,
                         data=json.dumps(self.airport_data))
        self.client.post('api/airport',
                         headers=self.header,
                         data=json.dumps(self.arrival_airport_data))
        self.client.post('api/airplane',
                         headers=self.header,
                         data=json.dumps(self.airplane_data))
        return self.client.post('api/flight',
                                headers=self.header,
                                data=json.dumps(self.flight_data))

    def test_admin_flight_addition(self):
        """Test adding flight by admin works correcty"""
        res = self.create_flight()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Flight schedule added successfully")
        self.assertEqual(res.status_code, 201)

    def test_user_flight_addition(self):
        """Test adding flight by user is not possible"""
        self.get_login_token()
        res = self.client.post('api/flight',
                               headers=self.header,
                               data=json.dumps(self.flight_data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Forbidden, Admins only!")
        self.assertEqual(res.status_code, 403)

    def test_get_available_flights(self):
        """Test get all available flights"""
        self.create_flight()
        res = self.client.get('api/flight',
                              headers=self.header)
        result = json.loads(res.data.decode())
        self.assertTrue(result['flights'])
        self.assertEqual(res.status_code, 200)

    def test_get_no_flights(self):
        """Test get all flights before adding"""
        self.admin_login()
        res = self.client.get('api/flight',
                              headers=self.header)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "No data to display")
        self.assertEqual(res.status_code, 200)
