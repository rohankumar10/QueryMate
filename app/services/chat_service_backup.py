import asyncio
import os
import json
import base64
import requests
import uuid
from datetime import datetime
from app.utils.chat_connection import get_chat_connection
from concurrent.futures import ThreadPoolExecutor
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
from app.utils.create_response import create_response

# Initialize a ThreadPoolExecutor for running async tasks
executor = ThreadPoolExecutor()

async def async_db_inserts(input_question_text, question_id, chat_id, user_id, related_question_data):
    # Perform the async DB inserts
    await insert_data_to_db_new_chain(
        input_question_text, question_id, chat_id, user_id, related_question_data['all_question_list'],
        # Add the other required parameters
    )
    similar_questions = find_similar_questions(input_question_text)  # Assuming this is sync
    await insert_data_to_db_related_question(
        input_question_text, question_id, chat_id, user_id, related_question_data['related_question_list'],
        # Add the other required parameters
    )

def new_chat(input_question_text, question_id, chat_id, user_id, user_alias, user_location, start_time, media, media_type):
    headers, ENDPOINT = get_chat_connection()

    global_temperature = 0.7
    global_top_p = 0.95
    global_max_tokens = 800
    global_model = "gpt-4o"

    insert_data_to_db_question(input_question_text, question_id, chat_id, user_id, user_alias, user_location, start_time, media, media_type)

    conversation = [{"role": "system", "content": "You are a QueryMate, an AI friend to help you grow."}]

    # Synchronous call to assign chain ID and related data
    chain_id, is_new_chain, model, temperature, max_token, related_question_response, related_question_data = assign_chain_id(
        input_question_text, question_id, chat_id, user_id, start_time
    )

    if not is_new_chain:
        user_chat = fetch_user_chat_from_chain_id(chain_id)
        if user_chat:
            for question_text, response_text in user_chat:
                conversation.append({"role": "user", "content": [{"type": "text", "text": question_text}]})
                conversation.append({"role": "assistant", "content": [{"type": "text", "text": response_text}]})

    # Run async inserts in a separate thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_in_executor(executor, async_db_inserts, input_question_text, question_id, chat_id, user_id, related_question_data)

    # Prepare the conversation and payload
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
        # Make the request with streaming enabled
        with requests.post(ENDPOINT, headers=headers, json=payload, stream=True) as response:
            response.raise_for_status()  # Check for any request errors

            assistant_message = ""
            for chunk in response.iter_content(chunk_size=1024):  # Adjust chunk size as needed
                if chunk:
                    # Assuming the response is in JSON format and structured as expected
                    data = chunk.decode('utf-8')
                    if data:
                        response_data = json.loads(data)
                        assistant_message += response_data['choices'][0]['message']['content']

            print("Assistant:", assistant_message)

            # Insert data to the database
            insert_data_to_db_response(response_data, input_question_text, question_id, chat_id, user_id, user_alias, global_model)
            insert_data_to_db_chain(chain_id, input_question_text, question_id, chat_id, user_id, user_alias, user_location, start_time, media, media_type, global_model, global_temperature, global_max_tokens, response_data, related_question_data["related_question_text"])

            return create_response(
                status_code=200,
                message="Success",
                data={"assistant_message": assistant_message}
            )
    except requests.RequestException as e:
        print(f"Failed to make the request. Error: {e}")
        return create_response(status_code=400, message="Bad Request", data=None)
