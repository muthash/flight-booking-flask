[![Build Status](https://travis-ci.com/muthash/flight-booking-flask.svg?branch=develop)](https://travis-ci.com/muthash/flight-booking-flask)
[![Coverage Status](https://coveralls.io/repos/github/muthash/flight-booking-flask/badge.svg?branch=ch-test-coverage-167084620)](https://coveralls.io/github/muthash/flight-booking-flask?branch=ch-test-coverage-167084620)
[![Maintainability](https://api.codeclimate.com/v1/badges/fc6831fb0680bdd545a1/maintainability)](https://codeclimate.com/github/muthash/flight-booking-flask/maintainability)
## Flight Booking API
A flight booking flask API that provides users with ability to:
- Register for an account
- Login into registered account
- Logout from the account

    #### 1. Customer
    - Upload/Edit/Delete passport photographs 
    - Search for flights
    - Book available scheduled flights
    - Receive flight reminders via email 24 hours before flight

    #### 2. Airline Staff
    - Add new airplane in the system
    - Get a list of all airplanes
    - Add new airport in the system
    - Get a list of all airports
    - Add new flight shedules
    - Get all flight schedules
    - Change Status of flights
    - Get a list of flight bookings in a given day

### Prerequisites
- Python 3.6 or a later version
- Flask
- PostgreSQL
- Use pip to install all the project dependancies

### Installation
Clone the repo.
```
$ git clone https://github.com/muthash/flight-booking-flask.git
```
and cd into the folder:
```
$ /flight-booking-flask
```

### Virtual environment
Create a virtual environment:
```
python3 -m venv venv
```
Activate the environment
```
$ source venv/bin/activate
```

### Dependencies
Install package requirements to your environment.
```
pip install -r requirements.txt
```

### Env

Create a .env file in your root directory and add
```
source venv/bin/activate
export FLASK_APP="run.py"
export FLASK_ENV="development"
export SECRET="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
export DATABASE_URL="postgresql://username:password@localhost/database_name"
export TEST_DATABASE_URL="postgresql://username:password@localhost/test_database_name"
export APP_MAIL_USERNAME="email address to send reminder emails"
export APP_MAIL_PASSWORD="password to access the senders email"
export ADMIN_EMAIL="Flight attendant email address"
export ADMIN_NAME="Flight attendant name"
export ADMIN_PASSWORD="Flight attendant password"
```

activate the environment
```
source .env
```

### Database migration

Create two Databases in PostgreSQL:
- production database
- testing database

Run the following commands for the development database:
```
$ python manage.py db init

$ python manage.py db migrate

$ python manage.py db upgrade

```

### Create Admin User
```
$ python manage.py create_admin
```

### Create Images Folder
```
$ python manage.py create_folder
```

### Testing

To run tests perform the following
```
$ python manage.py test
```

To run tests with coverage perform the following:
```
$ python manage.py cov
```

### Start The Server

To start the server run the following command
```
flask run
```
The server will run on http://127.0.0.1:5000/

### Testing API on Postman

*Note* Ensure that after you succesfully login a user, you use the generated token in the authorization header for the endpoints that require authentication. Remeber to add Bearer before the token as shown:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9eyJpYXQiO 
```
### API endpoints

| Endpoint | Method |  Functionality | Authentication |
| --- | --- | --- | --- |
| /api/register | POST | Creates a user account | FALSE
| /api/login | POST | Logs in a user | TRUE
| /api/logout | POST | Logs out a user | TRUE
| /api/uploads/passport | PUT | Upload Passport Photograph | TRUE
| /api/uploads/passport | DELETE | Delete Passport Photograph | TRUE
| /api/airport | POST | Add a new airport | ADMIN
| /api/airport | GET | Retrieve all airports | TRUE
| /api/airplane | POST | Add a new aircraft | ADMIN
| /api/airplane | GET | Retrieve all aircrafts | TRUE
| /api/flight | POST | Add a new flight schedule | ADMIN
| /api/flight | GET | Add all flight schedules | TRUE
| /api/v1/booking/<flight_id> | POST | Book a flight | TRUE
| /api/v1/booking/<flight_id>?bdate=Jul 02 2020 | GET | Get flight booking for a particular day | TRUE

### Heroku Production Link
Interact with the hosted application using this link
https://flight-booking-flask.herokuapp.com/