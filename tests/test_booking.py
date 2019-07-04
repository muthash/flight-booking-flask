"""Test case for the booking creation functionality"""
import os
import json

from datetime import datetime

from tests.base_test import BaseTestCase


class TestBookingManipulation(BaseTestCase):
    """Test for Booking manipulation endpoint"""
    def crate_flight(self):
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
        self.client.post('api/flight',
                         headers=self.header,
                         data=json.dumps(self.flight_data))

    def make_booking(self, seat):
        self.get_login_token()
        return self.client.post('api/booking/1',
                                headers=self.header,
                                data=json.dumps(dict(seat=seat)))

    def test_economy_seat_booking(self):
        """Test making booking for economy seat works correcty"""
        self.crate_flight()
        res = self.make_booking(1)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Economy seat flight reservation successfull")
        self.assertEqual(res.status_code, 201)

    def test_business_seat_booking(self):
        """Test making booking for business seat works correcty"""
        self.crate_flight()
        res = self.make_booking(2)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Business seat flight reservation successfull")
        self.assertEqual(res.status_code, 201)

    def test_booking_unavailable_flight(self):
        """Test making booking for non existing flight"""
        res = self.make_booking(1)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Selected flight not available")
        self.assertEqual(res.status_code, 400)

    def test_get_daily_bookings(self):
        """Test getting a list of all reservations in a given day"""
        self.crate_flight()
        self.make_booking(1)
        self.make_booking(2)
        self.admin_login()
        res = self.client.get('api/booking/1',
                              headers=self.header)
        result = json.loads(res.data.decode())
        self.assertEqual(result['number_of_booking'], 2)
        self.assertEqual(res.status_code, 200)

    def test_get_unavaillable_flight_daily_bookings(self):
        """Test getting a booking for non existing flight"""
        self.admin_login()
        res = self.client.get('api/booking/1',
                              headers=self.header)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "Selected flight not available")
        self.assertEqual(res.status_code, 400)
