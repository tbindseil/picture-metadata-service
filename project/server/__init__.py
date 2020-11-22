import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

db = SQLAlchemy(app)

from project.server.api import add_blueprint, all_blueprint
app.register_blueprint(add_blueprint)
app.register_blueprint(all_blueprint)
