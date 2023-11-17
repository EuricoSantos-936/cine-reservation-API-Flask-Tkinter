from flask_bcrypt import Bcrypt
from api.orm.data_orm import db

bcrypt = Bcrypt()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    room = db.Column(db.Integer, nullable=False, unique=True)
    seats = db.Column(db.Integer, nullable=False)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_select = db.Column(db.String(100), db.ForeignKey('movie.room'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_active(self):
        return self.is_active
    
    def get_id(self):
        return str(self.id)
    
    def is_authenticated(self):
        return True
    

    