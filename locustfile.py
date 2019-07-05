import os
import json

from locust import TaskSet, task, HttpLocust, seq_task


class UserBehavior(TaskSet):
    """The @task decorator declares a locust task"""
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.token = ""
        self.headers = {'Content-Type': 'application/json'}

    def on_start(self):
        self.token = self.login()
        self.headers = {'Authorization': 'Bearer ' + self.token}

    def login(self):
        reg_data = {
            "email": os.getenv('ADMIN_EMAIL'),
            "password": os.getenv('ADMIN_PASSWORD')
        }
        res = self.client.post("/api/login", headers=self.headers,
                               data=json.dumps(reg_data))
        return json.loads(res._content)['access_token']

    @task()
    def login_(self):
        self.login()

    @seq_task(1)
    def post_aiport(self):
        airport_data = {
            "name": "JKIA",
            "country": "Kenya",
            "city": "Nairobi"
        }
        self.client.post('/api/airport',
                         headers=self.headers,
                         data=json.dumps(airport_data))

    @task()
    def get_aiport(self):
        self.client.get('/api/airport',
                        headers=self.headers)

    @seq_task(2)
    def post_aiplane(self):
        airplane_data = {
            "reg_number": "FKJL76T",
            "economy_seats": 50,
            "business_seats": 10,
            "first_class_seats": 5
        }
        self.client.post('/api/airplane',
                         headers=self.headers,
                         data=json.dumps(airplane_data))

    @seq_task(3)
    def post_flight(self):
        flight_data = {
            "departure_date": "Jul 06 2019 12:00PM",
            "departure_airport_id": 1,
            "arrival_date": "Jul 06 2019 11:00PM",
            "arrival_airport_id": 2,
            "airplane_id": 1
        }
        self.client.post('/api/flight',
                         headers=self.headers,
                         data=json.dumps(flight_data))

    @task()
    def post_booking(self):
        self.client.post('/api/booking/20',
                         headers=self.headers,
                         data=json.dumps(dict(seat=1)))

    @task()
    def get_index(self):
        self.client.get("/")


class ApiClient(HttpLocust):
    task_set = UserBehavior
    host = "https://flight-booking-flask.herokuapp.com"
    min_wait = 1000
    max_wait = 5000
