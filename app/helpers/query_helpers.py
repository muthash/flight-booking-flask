from app.auth.models import User


def search_email(email):
        return User.query.filter_by(email=email).first()


def save_user(email, name, password):
    user = User(email, name, password)
    user.save()
