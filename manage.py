import os
import unittest
import coverage
import datetime

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import db, create_app, ROOT_DIR
from app.auth.models import User
from app.bookings.models import Booking
from app.flights.models import Airport, Airplane, Flight


app = create_app(os.getenv('FLASK_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def create_admin():
    """Creates the admin user."""
    try:
        db.session.add(User(
            email=os.getenv('ADMIN_EMAIL'),
            name=os.getenv('ADMIN_NAME'),
            password=os.getenv('ADMIN_PASSWORD'),
            is_admin=True,
            confirmed=True)
        )
        db.session.commit()
    except Exception as e:
        print(str(e))


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(branch=True, include='app/*')
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    cov.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    cov.erase()


@manager.command
def create_folder():
    """create the images folder."""
    uploads_dir = os.path.join(ROOT_DIR, 'images')
    try:
        os.makedirs(uploads_dir)
        print("Folder created successfully")
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    manager.run()
