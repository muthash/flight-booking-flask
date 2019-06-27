[![Build Status](https://travis-ci.com/muthash/flight-booking-flask.svg?branch=develop)](https://travis-ci.com/muthash/flight-booking-flask)
[![Coverage Status](https://coveralls.io/repos/github/muthash/flight-booking-flask/badge.svg?branch=develop)](https://coveralls.io/github/muthash/flight-booking-flask?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/fc6831fb0680bdd545a1/maintainability)](https://codeclimate.com/github/muthash/flight-booking-flask/maintainability)
## Flight Booking API
A flight booking flask API that provides users with ability to:
- Register for an account
- Login into registered account
- Logout from the account

    #### 1. Customer
    - Search for flights
    - Book available scheduled flights
    - Get all customer bookings
    - Filter specific bookings

    #### 2. Airline Staff
    - Create new flight shedules
    - Change Status of flights
    - Add new airplane in the system
    - Add new airport in the system
    - Filter flight schedules by date
    - View all daily flights
    - View Flight booking status

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
```

activate the environment
```
source .env
```

### Database migration

Create two Databases in PostgreSQL:
- production database
- testing database

Run the following commands for each database:
```
python manage.py db init

python manage.py db migrate

python manage.py db upgrade

```

### Testing

To set up unit testing environment:
```
$ pip install nose
$ pip install coverage
```

To run tests perform the following:
```
$ nosetests --with-coverage
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