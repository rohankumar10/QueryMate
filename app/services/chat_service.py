import asyncio
import os
import json
import base64
import requests
from flask import Flask, request
from flask_socketio import SocketIO, emit
from app.socket import socketio
from datetime import datetime
from flask_cors import CORS, cross_origin
from app.utils.chat_connection import get_chat_connection
from app.utils.helper_functions import (
    insert_data_to_db_question,
    insert_data_to_db_new_chain,
    insert_data_to_db_chain,
    insert_data_to_db_response,
    insert_data_to_db_related_question,
    fetch_user_chat_from_chain_id,
    assign_chain_id,
    find_similar_questions,
)


async def async_db_inserts(input_question_text, question_id, chat_id, user_id, related_question_data):
    await insert_data_to_db_new_chain(
        input_question_text, question_id, chat_id, user_id, related_question_data['all_question_list'],
        # Add the other required parameters
    )
    similar_questions = find_similar_questions(input_question_text)
    await insert_data_to_db_related_question(
        input_question_text, question_id, chat_id, user_id, related_question_data['related_question_list'],
        # Add the other required parameters
    )

@socketio.on('new_chat')
def new_chat(input_question_text, question_id, chat_id, user_id, user_alias, user_location, start_time, media, media_type):

    headers, ENDPOINT = get_chat_connection()

    global_temperature = 0.7
    global_top_p = 0.95
    global_max_tokens = 800
    global_model = "gpt-4o"

    insert_data_to_db_question(input_question_text, question_id, chat_id, user_id, user_alias, user_location, start_time, media, media_type)

    conversation = [{"role": "system", "content": "You are a QueryMate, an AI friend to help you grow."}]

    chain_id, is_new_chain, model, temperature, max_token, related_question_response, related_question_data = assign_chain_id(
        input_question_text, question_id, chat_id, user_id, start_time
    )

    if not is_new_chain:
        user_chat = fetch_user_chat_from_chain_id(chain_id)
        if user_chat:
            for question_text, response_text in user_chat:
                conversation.append({"role": "user", "content": [{"type": "text", "text": question_text}]})
                conversation.append({"role": "assistant", "content": [{"type": "text", "text": response_text}]})

    if os.path.isfile(media):
        with open(media, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('ascii')
        conversation.append({
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
                {"type": "text", "text": input_question_text}
            ]
        })
    else:
        conversation.append({"role": "user", "content": [{"type": "text", "text": input_question_text}]})

    payload = {
        "messages": conversation,
        "temperature": global_temperature,
        "top_p": global_top_p,
        "max_tokens": global_max_tokens,
        "stop": "exit"
    }

    try:
        with requests.post(ENDPOINT, headers=headers, json=payload, stream=True) as response:
            response.raise_for_status()  # Check for any request errors

            incomplete_data = ""
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    data = chunk.decode('utf-8')
                    incomplete_data += data

                    try:
                        response_data = json.loads(incomplete_data)
                        incomplete_data = ""
                        
                        print(response_data['choices'][0]['message']['content'])
                        # Emit the response back to the client
                        socketio.emit('assistant_message', {"message": response_data['choices'][0]['message']['content']})

                    except json.JSONDecodeError:
                        continue

            # Finalize database insertion after streaming ends
            insert_data_to_db_response(response_data, input_question_text, question_id, chat_id, user_id, user_alias, global_model)
            insert_data_to_db_chain(chain_id, input_question_text, question_id, chat_id, user_id, user_alias, user_location, start_time, media, media_type, global_model, global_temperature, global_max_tokens, response_data, related_question_data["related_question_text"])

    except requests.RequestException as e:
        print(f"Failed to make the request. Error: {e}")
        socketio.emit('error', {"error": "Bad Request"})
