from flask import Flask
from Portfolio.Blueprints.portfolio.blueprint import blueprint
from Portfolio.Blueprints.login.auth import auth
from Portfolio.Blueprints.crud.crud import crud
from datetime import timedelta

def create_app():
    app = Flask(__name__)

    app.secret_key = 'my super secret random very random super key'

    app.permanent_session_lifetime = timedelta(days=1)

    app.register_blueprint(blueprint, url_prefix='/')

    app.register_blueprint(auth, url_prefix='/')

    app.register_blueprint(crud, url_prefix='/')

    return app