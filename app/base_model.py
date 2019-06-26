from app import db


class BaseModel(db.Model):
    """Base model from which all other models will inherit from"""
    __abstract__ = True

    def save(self):
        """Save the given object to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes a given object"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update(class_instance, **kwargs):
        """Update selected columns in given row in a table"""
        for column in kwargs:
            setattr(class_instance, column, kwargs[column])
        db.session.commit()
