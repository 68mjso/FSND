import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "postgresql:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    db.app = app
    db.init_app(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    release_date = db.Column(db.DateTime, nullable=False)

    actor_id = db.Column(db.Integer, db.ForeignKey("Actor.id"), nullable=False)

    def get(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        }

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        finally:
            db.session.close()
        return True

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        finally:
            db.session.close()
        return True

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        finally:
            db.session.close()
        return True

    def __repr__(self):
        return json.dumps(self.get())


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    age = db.Column(db.Interger)
    gender = db.Column(db.String(120))

    movies = db.relationship("Movie", backref="actor", lazy=True)

    def get(self):
        return {
            "id": self.id,
            "title": self.title,
            "age": self.age,
            "gender": self.gender,
        }

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        finally:
            db.session.close()
        return True

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        finally:
            db.session.close()
        return True

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        finally:
            db.session.close()
        return True

    def __repr__(self):
        return json.dumps(self.get())
