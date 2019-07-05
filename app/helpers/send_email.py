import os
import atexit
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask_mail import Message

from app import mail
from app.helpers.query_helpers import get_tomorrow_flights


def get_booked_flights():
    logging.info('Fetching tomorrows flights from the database')
    flights = []
    flights_to = get_tomorrow_flights()
    for flight in flights:
        total_booked = flight.booked_business + flight.booked_economy
        total_seats = flight.airplane.total_seats
        if (total_seats - total_booked) != total_seats:
            flights.append(flight)
    return flights


def create_message_list(flights):
    messages = []
    for flight in flights:
        message = Message(
            subject='Flight Reservation Reminder',
            recipients=[flight.bookings.owner.email],
            html=(f'Hello {flight.bookings.owner.email.name},'
                  f'<p> This is to remind you of your scheduled flight <b>{flight.airplane.reg_number}</b>'
                  f'from <b>{flight.airport.name}</b> on <b>{flight.departure_date}</b> </p>'
                  f'<p> Please check in for your flight three hours before departure time</p>'
                  f'<p> Thank you </p>')
                )
        messages.append(message)
    return messages


def send_reminder_email():
    flights = get_booked_flights()
    if not flights:
        logging.info("There are no bookings for tommorrow flights yet")
    else:
        logging.info("creating the mailing lists ...")
        messages = create_message_list(flights)

        logging.info("connecting to the mail server ...")
        with mail.connect() as conn:
            for message in messages:
                try:
                    conn.send(message)
                    "sending success: " + message.recipients
                except Exception as e:
                    logging.exception("sending failed: " + message.recipients)


def background_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=send_reminder_email,
        trigger=IntervalTrigger(start_date='2019-07-02 03:00:00', days=1),
        id='reminder_email_job',
        name='sending emails in the background',
        replace_existing=True)
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    atexit.register(lambda: scheduler.shutdown())
