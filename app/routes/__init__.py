from flask import Blueprint

chat_bp = Blueprint("chat", __name__)

from .chat_routes import *
