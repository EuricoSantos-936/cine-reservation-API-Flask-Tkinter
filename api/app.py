from flask import Flask
from flask_login import LoginManager
from api.models.models import User
from api.views.views import main_view
from api.orm import data_orm
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_view, url_prefix="")
    app.config.from_pyfile('config.py')
    data_orm.init_app(app)
    
    Migrate(app, data_orm.db)

    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) 

    with app.app_context():
        data_orm.db.create_all()

    return app