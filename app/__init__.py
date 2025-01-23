from flask import Flask
from .socket import socketio  # Import from the new socket module
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Initialize the SocketIO instance
    socketio.init_app(app, cors_allowed_origins="http://localhost:8000")
    CORS(app)
    
    # Register your blueprints here
    from .routes import chat_bp
    app.register_blueprint(chat_bp)

    return app
