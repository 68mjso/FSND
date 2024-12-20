from flask import Blueprint, jsonify, request, abort
from flask_cors import CORS, cross_origin
from models import Movie, Actor
from auth import requires_auth
from datetime import datetime

api = Blueprint("api", __name__)


@api.route("/movies", methods=["GET"])
@cross_origin()
@requires_auth(permission="view:movies")
def get_movies(_):
    movies = Movie.query.all()
    movies_res = [movie.get() for movie in movies]
    return jsonify({"status": 200, "data": movies_res}), 200


@api.route("/movies", methods=["POST"])
@cross_origin()
@requires_auth(permission="post:movies")
def insert_movie(_):
    data = request.json
    title = data.get("title")
    release_date = data.get("release_date")
    actors = data.get("actors")
    release_date = datetime.strptime(release_date, "%Y-%m-%d")
    movie = Movie(title=title, release_date=release_date)
    res = movie.insert(actors)
    if res is not True:
        return jsonify({"status": 400, "success": res}), 400
    return jsonify({"status": 200, "success": res}), 200


@api.route("/movies/<int:id>", methods=["PATCH"])
@cross_origin()
@requires_auth(permission="patch:movies")
def update_movie(_, id):
    movie: Movie = Movie.query.get(id)
    if movie is None:
        abort(404)
    data = request.json
    title = data.get("title")
    release_date = data.get("release_date")
    actors = data.get("actors")
    movie.title = title
    movie.release_date = datetime.strptime(release_date, "%Y-%m-%d")
    res = movie.update(actors)
    if res is not True:
        return jsonify({"status": 400, "success": res}), 400
    return jsonify({"status": 200, "success": res}), 200


@api.route("/movies/<int:id>", methods=["DELETE"])
@cross_origin()
@requires_auth(permission="delete:movies")
def delete_movie(_, id):
    movie: Movie = Movie.query.get(id)
    if movie is None:
        abort(404)
    res = movie.delete()
    if res is not True:
        return jsonify({"status": 400, "success": res}), 400
    return jsonify({"status": 200, "success": res}), 200


@api.route("/actors", methods=["GET"])
@cross_origin()
@requires_auth(permission="view:actors")
def get_actors(_):
    actors = Actor.query.all()
    actors_res = [actor.get() for actor in actors]
    return jsonify({"status": 200, "data": actors_res}), 200


@api.route("/actors", methods=["POST"])
@cross_origin()
@requires_auth(permission="post:actors")
def insert_actor(_):
    data = request.json
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    actor = Actor(name=name, age=age, gender=gender)
    res = actor.insert()
    if res is not True:
        return jsonify({"status": 400, "success": res}), 400
    return jsonify({"status": 200, "success": res}), 200


@api.route("/actors/<int:id>", methods=["PATCH"])
@cross_origin()
@requires_auth(permission="patch:actors")
def update_actor(_, id):
    actor: Actor = Actor.query.get(id)
    if actor is None:
        abort(404)
    data = request.json
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    actor.name = name
    actor.age = age
    actor.gender = gender
    res = actor.update()
    if res is not True:
        return jsonify({"status": 400, "success": res}), 400
    return jsonify({"status": 200, "success": res}), 200


@api.route("/actors/<int:id>", methods=["DELETE"])
@cross_origin()
@requires_auth(permission="delete:actors")
def delete_actor(_, id):
    actor: Actor = Actor.query.get(id)
    if actor is None:
        abort(404)
    res = actor.delete()
    if res is not True:
        return jsonify({"status": 400, "success": res}), 400
    return jsonify({"status": 200, "success": res}), 200
