from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from api.models import models
from api.orm.data_orm import db

main_view = Blueprint("main_view", __name__)


# Rota para criar um novo usuário
@main_view.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        existing_user = models.User.query.filter_by(username=username).first()
        if existing_user:
            return (
                jsonify({"message": "O utilizador já existe"}),
                409,
            )
        else:
            user = models.User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "Utilizador criado com sucesso"}), 201
    else:
        return jsonify({"message": "Utilizador ou password são obrigatórios"}), 400


# Rota para redefinir a senha de um usuário
@main_view.route("/users/<int:user_id>/reset_password", methods=["POST"])
def reset_password(user_id):
    user = models.User.query.get(user_id)
    if user:
        data = request.get_json()
        new_password = data.get("new_password")

        if new_password is not None:
            user.set_password(new_password)  # Correção aqui
            db.session.commit()
            return jsonify({"message": "Password reposta com sucesso"}), 200
        else:
            return jsonify({"message": "É obrigatória uma password"}), 400
    else:
        return jsonify({"message": "Utilizador não encontrado"}), 404


# Rota para fazer login
@main_view.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = models.User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Login com sucesso"}), 200
    else:
        return (
            jsonify({"message": "Credenciais invalidas, password ou username incorretos"}),
            401,
        )


# Rota para fazer logout
@main_view.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout com sucesso."}), 200


# Rota para ver todos os filmes
@main_view.route("/movies", methods=["GET"])
def get_movies():
    movies = models.Movie.query.all()

    if not movies:
        return jsonify({"message": "Nenhum filme disponível atualmente."}), 404

    movie_list = [{"id": movie.id, "title": movie.title} for movie in movies]
    return jsonify(movie_list)


# Rota para ver um filme por id
@main_view.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = models.Movie.query.get(movie_id)
    if movie:
        return jsonify(
            {"id": movie.id, "title": movie.title, "description": movie.description}
        )
    else:
        return jsonify({"message": "Filme não encontrado"}), 404


# Rota para fazer uma reserva
@main_view.route("/reservations", methods=["POST"])
@login_required
def create_reservation():
    data = request.get_json()
    movie_id = data.get("movie_id")
    user_id = current_user.get_id()

    movie = models.Movie.query.get(movie_id)
    if not movie:
        return jsonify({"message": "Filme não encontrado"}), 404

    if movie.seats <= 0:
        return jsonify({"message": "Não há lugares disponíveis para este filme"}), 400

    movie.seats -= 1

    reservation = models.Reservation(
        movie_id=movie_id,
        user_id=user_id,
        room_select=movie.room
    )
    db.session.add(reservation)
    db.session.commit()

    return jsonify({"message": "Reserva criada com sucesso"}), 201

# Rota para adicionar um filme em exibição
@main_view.route("/showing_movies", methods=["POST"])
def add_showing_movie():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    room = data.get("room")
    seats = data.get("seats")

    if not title or not room or not seats:
        return jsonify({"message": "Titulo, sala, lugares são obrigatórios"}), 400

    existing_movie = models.Movie.query.filter_by(room=room).first()
    if existing_movie:
        return jsonify({"message": "Sala já está em utilização."}), 400

    new_movie = models.Movie(
        title=title, description=description, room=room, seats=seats
    )
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({"message": "Filme adicionado com sucesso"}), 201


#Rota para apagar filme, ao apagar filme apaga as reservas
@main_view.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    movie = models.Movie.query.get(movie_id)
    if not movie:
        return jsonify({"message": "Filme não encontrado"}), 404
    
    models.Reservation.query.filter_by(movie_id=movie_id).delete()

    db.session.delete(movie)
    db.session.commit()

    return jsonify({"message": "Filme removido com sucesso"}), 200