import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import db, create_app
from app.auth.models import User
from app.bookings.models import Booking, EmailSchedule
from app.flights.models import Airport, Airplane, Flight

app = create_app(os.getenv('FLASK_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()