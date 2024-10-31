import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1@localhost:5432/postgres"
# database_path = "postgresql:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    db.app = app
    db.init_app(app)


class MovieActor(db.Model):
    __tablename__ = "movie_actor"

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey("actor.id"), nullable=False)


class Movie(db.Model):

    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    release_date = db.Column(db.DateTime, nullable=False)

    actors = db.relationship(
        "Actor", secondary="movie_actor", backref=db.backref("movies", lazy=True)
    )

    def get(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "actors": [actor.get() for actor in self.actors],
        }

    def insert(self, actors):
        try:
            db.session.add(self)
            for id in actors:
                actor = Actor.query.get(id)
                if actor not in self.actors:
                    self.actors.append(actor)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        finally:
            db.session.close()
        return True

    def update(self, actors):
        try:
            self.actors = []
            for id in actors:
                actor = Actor.query.get(id)
                if actor not in self.actors:
                    self.actors.append(actor)
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

    __tablename__ = "actor"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(120))

    def get(self):
        return {
            "id": self.id,
            "name": self.name,
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
