from flask import request
from flask_socketio import SocketIO, emit
from . import chat_bp
from app.services.chat_service import new_chat
from app.socket import socketio
import uuid
from datetime import datetime
from flask_cors import CORS, cross_origin

@chat_bp.route('/new_chat', methods=['POST'])
def new_chat_endpoint():
    # This function can remain for HTTP requests if needed
    data = request.json
    print(data)
    input_question_text = data.get('question_text')
    question_id = data.get('question_id', str(uuid.uuid4()))
    chat_id = data.get('chat_id', str(uuid.uuid4()))
    user_id = data.get('user_id')
    user_alias = data.get('user_alias')
    user_location = data.get('user_location')
    start_time = data.get('start_time', datetime.now().isoformat())
    media = data.get('media', '')
    media_type = data.get('media_type', '')

    # Call the new_chat function and return its response
    return new_chat(input_question_text, question_id, chat_id, user_id, user_alias, user_location, start_time, media, media_type)

# New WebSocket event handler
@socketio.on('new_chat_event')
def handle_new_chat_event(data):
    print(data)
    input_question_text = data.get('question_text')
    question_id = data.get('question_id', str(uuid.uuid4()))
    chat_id = data.get('chat_id', str(uuid.uuid4()))
    user_id = data.get('user_id')
    user_alias = data.get('user_alias')
    user_location = data.get('user_location')
    start_time = data.get('start_time', datetime.now().isoformat())
    media = data.get('media', '')
    media_type = data.get('media_type', '')

    # Call the new_chat function and get the response
    response = new_chat(input_question_text, question_id, chat_id, user_id, user_alias, user_location, start_time, media, media_type)

    # Emit the response back to the client
    emit('new_chat_response', response)
