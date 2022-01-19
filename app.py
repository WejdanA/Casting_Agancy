import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movie, Actor, Cast, setup_db
from auth import AuthError, requires_auth


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # implementing CRUD for movies model
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        return jsonify({
            "success": True,
            "movies": [movie.format() for movie in movies]})

    @app.route('/movies', methods=['POST'])
    @requires_auth("post:movie")
    def post_movie(payload):
        try:
            name = request.get_json()['name']
            releaseDate = request.get_json()['releaseDate']
            movie = Movie(name=name, releaseDate=releaseDate)
            movie.insert()
            newMovie = Movie.query.filter_by(name=name).one_or_none()
        except Exception:
            abort(400)
        return jsonify({
            "success": True,
            'movie': newMovie.format()})

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth("patch:movie")
    def edit_movie(payload, id):
        movie = Movie.query.filter_by(id=id).one_or_none()
        if movie is None:
            abort(404)

        try:
            name = request.get_json()['name']
            releaseDate = request.get_json()['releaseDate']
            movie.name = name
            movie.releaseDate = releaseDate
            movie.update()
        except Exception:
            abort(400)
        newMovie = Movie.query.filter_by(id=id).one_or_none()
        return jsonify({
            "success": True,
            'movie': newMovie.format()
            })

    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth("delete:movie")
    def delete_movie(payload, id):
        movie = Movie.query.filter_by(id=id).one_or_none()
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
            "success": True,
            'delete': id
            })

    # implement CRUD for Actor models
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        return jsonify({
            "success": True,
            "actors": [actor.format() for actor in actors]
            })

    @app.route('/actors', methods=['POST'])
    @requires_auth("post:actor")
    def post_actor(payload):
        try:
            name = request.get_json()['name']
            gender = request.get_json()['gender']
            actor = Actor(name=name, gender=gender)
            actor.insert()
            newActor = Actor.query.filter_by(name=name).one_or_none()
        except Exception:
            abort(400)
        return jsonify({
            "success": True,
            'actor': newActor.format()
            })

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth("patch:actor")
    def edit_actor(payload, id):
        actor = Actor.query.filter_by(id=id).one_or_none()
        if actor is None:
            abort(404)

        try:
            name = request.get_json()['name']
            gender = request.get_json()['gender']
            actor.name = name
            actor.gender = gender
            actor.update()
        except Exception:
            abort(400)
        newActor = Actor.query.filter_by(id=id).one_or_none()
        return jsonify({
            "success": True,
            'actor': newActor.format()
            })

    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth("delete:actor")
    def delete_actor(payload, id):
        actor = Actor.query.filter_by(id=id).one_or_none()
        if actor is None:
            abort(404)

        actor.delete()
        return jsonify({
            "success": True,
            'delete': id
            })

    # implement CRUD for Cast models
    @app.route('/cast', methods=['GET'])
    @requires_auth('get:cast')
    def get_cast(payload):
        casts = Cast.query.all()
        return jsonify({
            "success": True,
            "casts": [cast.format() for cast in casts]
            })

    # get all the movies for specific actors
    @app.route('/actors/<actor_id>/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies_by_actor(payload, actor_id):
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)

        casts = actor.cast
        movies = {Movie.query.get(cast.movie_id) for cast in casts}
        return jsonify({
            "success": True,
            "movies": [movie.format() for movie in movies]
            })

    # get all the actors who works in specific movie
    @app.route('/movies/<movie_id>/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors_by_movie(payload, movie_id):
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)
        casts = movie.cast
        actors = {Actor.query.get(cast.actor.id) for cast in casts}
        return jsonify({
            "success": True,
            "actors": [actor.format() for actor in actors]
            })

    @app.route('/cast', methods=['POST'])
    @requires_auth("post:cast")
    def post_cast(payload):
        try:
            movie_id = request.get_json()['movie_id']
            actor_id = request.get_json()['actor_id']
            cast = Cast(movie_id=movie_id, actor_id=actor_id)
            cast.insert()
        except Exception:
            abort(400)
        return jsonify({
            "success": True
            })

    @app.route('/cast/<id>', methods=['DELETE'])
    @requires_auth("delete:cast")
    def delete_cast(payload, id):
        cast = Cast.query.filter_by(id=id).one_or_none()
        if cast is None:
            abort(404)
        cast.delete()
        return jsonify({
            "success": True,
            'delete': id
            })

    # Error Handling
    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
            }), 400

    @app.errorhandler(404)
    def NotFound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "The request resource is not found"
            }), 404

    @app.errorhandler(405)
    def NotFound(error):
        return jsonify({
             "success": False,
             "error": 405,
             "message": "Method Not Allowed"
             }), 405

    # Reference to https://auth0.com/docs/
    # quickstart/backend/python/01-authorization
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
