from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json
import os
# https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre
# DATABASE_URL='postgresql://postgres:12345@localhost:5432/postgres'
database_path = os.environ.get('DATABASE_URL')
print(database_path)
db = SQLAlchemy()

'''
setup_db(app)
binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.drop_all()
    # db.create_all()


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    gender = db.Column(db.String(), nullable=False)
    cast = db.relationship('Cast', backref='actor', lazy=True,
                           passive_deletes=True)

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender}

    def insert(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()

    def update(self):
        db.session.commit()
        db.session.close()


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    releaseDate = db.Column(db.DateTime, nullable=False)
    cast = db.relationship('Cast', backref='movie', lazy=True,
                           passive_deletes=True)

    def __init__(self, name, releaseDate):
        self.name = name
        self.releaseDate = releaseDate

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'releaseDate': self.releaseDate}

    def insert(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()

    def update(self):
        db.session.commit()
        db.session.close()


class Cast(db.Model):
    __tablename__ = 'Cast'

    id = db.Column(Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id',
                         ondelete='CASCADE'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('Actor.id',
                         ondelete='CASCADE'), nullable=False)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id}

    def insert(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()

    def update(self):
        db.session.commit()
        db.session.close()
