from flask import Flask
from flask_app.config.config import Config

app = Flask(__name__)
app.config.from_object(Config)