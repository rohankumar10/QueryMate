from app import create_app, socketio  # Import socketio here
import os

app = create_app()

if __name__ == "__main__":
    port = os.getenv("PORT", 5000)  # Default to 5000 if PORT is not set
    socketio.run(app, host='0.0.0.0', port=int(port), debug=True)  # Use socketio.run
