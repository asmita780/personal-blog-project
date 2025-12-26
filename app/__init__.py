from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os


db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "MY_SECRET_KEY"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["DATABASE_TRACK_MODIFICATION"] = False
    app.config["UPLOAD_FOLDER"] = "app/static/images" #tells flask where to store file

    db.__init__(app)

    from app.models import UserDetails, UserPost
    
    with app.app_context():
        db.create_all()

    from app.routes.auths import auth_bp
    from app.routes.tasks import task_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app
