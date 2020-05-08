from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.movies import Movie


class MovieResource(Resource):
    def get(self, id):
        abort_if_movie_not_found(id)
        session = db_session.create_session()
        movie = session.query(Movie).get(id)
        return jsonify({'movie': movie.to_dict(
            only=('genre', 'name', 'year', 'duration', 'watched', 'timecode', 'review'))})

    def delete(self, id):
        abort_if_movie_not_found(id)
        session = db_session.create_session()
        movie = session.query(Movie).get(id)
        session.delete(movie)
        session.commit()
        return jsonify({'success': 'OK'})


class MovieListResource(Resource):
    def get(self):
        session = db_session.create_session()
        movie = session.query(Movie).all()
        return jsonify({'movie': [item.to_dict(
            only=('genre', 'name', 'year', 'duration', 'watched', 'timecode', 'review')) for item in movie]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        movie = Movie()
        movie.name = args['name'],
        movie.genre = args['genre'],
        movie.id_author = args['id_author'],
        movie.year = args['year'],
        movie.duration = args['duration'],
        movie.watched = args['watched'],
        movie.timecode = args['timecode'],
        movie.review = args['review']
        session.add(movie)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_movie_not_found(movie_id):
    session = db_session.create_session()
    movie = session.query(Movie).get(movie_id)
    if not movie:
        abort(404, message=f"Movie {movie_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('id_author', required=True, type=int)
parser.add_argument('name', required=True)
parser.add_argument('genre', required=True)
parser.add_argument('year', required=True)
parser.add_argument('duration', required=True)
parser.add_argument('watched', required=True, type=bool)
parser.add_argument('timecode', required=True)
parser.add_argument('review', required=True)


