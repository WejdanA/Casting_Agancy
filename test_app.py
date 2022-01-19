import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, Cast, db
import random


class CapstoneTestCase(unittest.TestCase):
    """This class represents the casting agancy test case"""
    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""
        cls.app = create_app()
        cls.client = cls.app.test_client
        # update the database name ,user name and passwords of
        # database to connect to your database
        cls.db_name = "test"
        cls.database_path = "postgresql://{}:{}@{}/{}".format('postgres',
                                                              '12345',
                                                              'localhost:5432',
                                                              cls.db_name)
        setup_db(cls.app, cls.database_path)
        db.drop_all()
        db.create_all()
        movie = Movie(name='avengers', releaseDate='01/01/2004')
        movie.insert()
        movie = Movie(name='avengers infinity war', releaseDate='01/01/2004')
        movie.insert()
        actor = Actor(name='Scarlett Johansson', gender='F')
        actor.insert()
        actor = Actor(name='Chris Evan', gender='M')
        actor.insert()
        cast = Cast(movie_id=1, actor_id=1)
        cast.insert()
        cast = Cast(movie_id=1, actor_id=1)
        cast.insert()
        cls.access_ExPr = os.environ.get('EX_PR_ACCESS_TOKEN')
        cls.access_castingAss = os.environ.get('CASTING_ASS_ACCESS_TOKEN')
        cls.access_castingDir = os.environ.get('CASTING_DIR_ACCESS_TOKEN')
        cls.headers_ExPr = {"Authorization": 'bearer ' + cls.access_ExPr}
        cls.headers_castingAss = {"Authorization":
                                  'bearer '+cls.access_castingAss}
        cls.headers_castingDir = {"Authorization":
                                  'bearer '+cls.access_castingDir}

    def tearDown(self):
        """Executed after reach test"""
        pass

    """ testing movie model endpoint"""
    def test_for_get_movies(self):
        res = self.client().get('/movies', headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_for_post_new_movie(self):
        res = self.client().post('/movies', json={'name': 'Iron Man',
                                                  'releaseDate': '01/01/2008'},
                                 headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_400_for_faild_movie_posting(self):
        res = self.client().post('/movies', json={'name': 'Iron Man'},
                                 headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_for_edit_movies(self):
        res = self.client().patch('/movies/1', json={'name': 'Iron ManXX',
                                                     'releaseDate':
                                                     '01/01/2088'},
                                  headers=self.headers_ExPr)
        data = json.loads(res.data)
        edit_movie = Movie.query.filter_by(id=1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'], {'id': 1, 'name': 'Iron ManXX',
                                         'releaseDate':
                                         'Thu, 01 Jan 2088 00:00:00 GMT'})

    def test_404_for_edit_notfound_movie(self):
        res = self.client().patch('/movies/1000', json={'name': 'Iron Man2',
                                                        'releaseDate':
                                                        '01/01/2008'},
                                  headers=self.headers_ExPr)
        data = json.loads(res.data)
        edit_movie = Movie.query.filter_by(id=1000).one_or_none()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(edit_movie, None)

    def test_for_delete_movie(self):
        res = self.client().delete('/movies/2', headers=self.headers_ExPr)
        data = json.loads(res.data)
        deleted_movie = Movie.query.filter_by(id=2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(deleted_movie, None)

    def test_404_for_delete_notfound_movie(self):
        res = self.client().delete('/movies/1000', headers=self.headers_ExPr)
        data = json.loads(res.data)
        deleted_movie = Movie.query.filter_by(id=1000).one_or_none()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(deleted_movie, None)

    """ testing actor model endpoint"""
    def test_for_get_actor(self):
        res = self.client().get('/actors', headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_for_post_new_actor(self):
        res = self.client().post('/actors', json={'name': 'Robert Downey Jr.',
                                                  'gender': 'M'},
                                 headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_400_for_failed_actor_posting(self):
        res = self.client().post('/actors', json={'name': 'Robert Downey Jr.'},
                                 headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_for_patch_actors(self):
        res = self.client().patch('/actors/1', json={'name': 'Robert Downey',
                                                     'gender': 'M'},
                                  headers=self.headers_ExPr)
        data = json.loads(res.data)
        edit_actor = Actor.query.filter_by(id=1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], {'id': 1, 'name': 'Robert Downey',
                                         'gender': 'M'})

    def test_404_for_edit_notfound_actor(self):
        res = self.client().patch('/actors/1000', headers=self.headers_ExPr)
        data = json.loads(res.data)
        edit_actor = Actor.query.filter_by(id=1000).one_or_none()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(edit_actor, None)

    def test_for_delete_actor(self):
        res = self.client().delete('/actors/2', headers=self.headers_ExPr)
        data = json.loads(res.data)
        deleted_actor = Actor.query.filter_by(id=2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(deleted_actor, None)

    def test_404_for_delete_notfound_actor(self):
        res = self.client().delete('/actors/1000', headers=self.headers_ExPr)
        data = json.loads(res.data)
        deleted_actor = Actor.query.filter_by(id=1000).one_or_none()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(deleted_actor, None)

    """ testing cast model endpoint"""
    def test_for_get_cast(self):
        res = self.client().get('/cast', headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['casts']))

    def test_for_get__movies_by_actor(self):
        res = self.client().get('actors/1/movies', headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_404_for_get_movies_by_Notfound_actor(self):
        res = self.client().get('actors/1000/movies',
                                headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_for_get__actors_by_movie(self):
        res = self.client().get('movies/1/actors',
                                headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_404_for_get_actor_by_Notfound_movie(self):
        res = self.client().get('movies/1000/actors',
                                headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_for_post_new_cast(self):
        res = self.client().post('/cast', json={'movie_id': 1, 'actor_id': 1},
                                 headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_for_failed_cast_posting(self):
        # this to test the endpoing in case  not existing actor or movie ids
        res = self.client().post('/cast', json={'movie_id': 1000,
                                                'actor_id': 1000},
                                 headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_for_delete_cast(self):
        res = self.client().delete('/cast/2', headers=self.headers_ExPr)
        data = json.loads(res.data)
        deleted_cast = Cast.query.filter_by(id=2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(deleted_cast, None)

    def test_404_for_delete_notfound_cast(self):
        res = self.client().delete('/cast/1000', headers=self.headers_ExPr)
        data = json.loads(res.data)
        deleted_cast = Cast.query.filter_by(id=1000).one_or_none()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(deleted_cast, None)

    """ testing casting assistant role """
    def test_for_get_actor_by_castingAss(self):
        res = self.client().get('/actors', headers=self.headers_castingAss)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_for_post_new_actor_by_castingAss(self):
        res = self.client().post('/actors', json={'name': 'XX.',
                                                  'gender': 'M'},
                                 headers=self.headers_castingAss)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')

    """ testing casting director role """
    def test_for_post_new_actor_by_castingDirector(self):
        res = self.client().post('/actors', json={'name': 'XXXX.',
                                                  'gender': 'M'},
                                 headers=self.headers_castingDir)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_for_post_new_movie_by_castingDirector(self):
        res = self.client().post('/movies', json={'name': 'Iron Man',
                                                  'releaseDate': '01/01/2008'},
                                 headers=self.headers_castingDir)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')

    """ testing Executive Producer role """
    def test_for_post_new_movie_by_ExecutiveProducer(self):
        res = self.client().post('/movies', json={'name': 'XXXX',
                                                  'releaseDate': '01/01/2008'},
                                 headers=self.headers_ExPr)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_for_post_new_movie_without_AuthorisationHeader(self):
        res = self.client().post('/movies', json={'name': 'XXX XX',
                                                  'releaseDate': '01/01/2008'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
