import uuid
import requests
import os
from datetime import datetime
from app.utils.cosmos_connection import get_db_container
from app.utils.chat_connection import get_chat_connection


def insert_data_to_db_question(question_text, question_id, chat_id, user_id, user_alias, user_location, start_time, media, media_type):

    container = get_db_container("NewQuestion")

    # Generate a unique ID using UUID
    unique_id = str(uuid.uuid4())

    # Prepare the document to be stored
    document = {
        "id": unique_id,
        "timestamp": datetime.now().isoformat(),
        "question_id": question_id,
        "chat_id":chat_id,
        "user_id":user_id,
        "user_alias": user_alias,
        "user_location": user_location,
        "start_time": start_time,
        "media": media,
        "media_type": media_type,
        "question_text": question_text
    }

    # Store the document in Azure Cosmos DB
    try:
        container.create_item(body=document)
        print("Question Data stored successfully in Azure Cosmos DB.")
    except exceptions.CosmosHttpResponseError as e:
        print(f"An error occurred: {e.message}")

def insert_data_to_db_new_chain(question_text, question_id, chat_id, user_id, all_questions, start_time, model, temperature, max_token, response, is_question_related, related_question_id, related_question_text):
    container = get_db_container("NewChain")
    # Extract the response values
    try:
        completion_tokens = response['usage']['completion_tokens']
        prompt_tokens = response['usage']['prompt_tokens']
        total_tokens = response['usage']['total_tokens']
        content = response['choices'][0]['message']['content']
        response_id = response['id']
    except Exception as e:
        print(f"Error extracting response values: {e}")
        completion_tokens = 0
        prompt_tokens = 0
        total_tokens = 0
        content = 0
        response_id = 0
        
    print(content, response_id)
    # Generate a unique ID using UUID
    unique_id = str(uuid.uuid4())

    # Prepare the document to be stored
    document = {
        "id": unique_id,
        "timestamp": datetime.now().isoformat(),
        "question_text": question_text,
        "question_id": question_id,
        "chat_id":chat_id,
        "user_id":user_id,
        "all_questions": all_questions,
        "start_time": start_time,
        "model":model,
        "role":"user",
        "max_token":max_token,
        "temperature": temperature,
        "token_used": total_tokens,
        "response_id":response_id,
        "is_question_related":is_question_related,
        "related_question_id":related_question_id,
        "related_question_text":related_question_text,
    }

    # Store the document in Azure Cosmos DB
    try:
        container.create_item(body=document)
        print("New chain Data stored successfully in Azure Cosmos DB.")
    except exceptions.CosmosHttpResponseError as e:
        print(f"An error occurred: {e.message}")


def insert_data_to_db_chain(chain_id, question_text, question_id, chat_id, user_id, user_alias, user_location, start_time, media, media_type, model, temperature, max_token, response, context_question):

    container = get_db_container("Chain")

    # Generate a unique ID using UUID
    unique_id = str(uuid.uuid4())

    # Extract the response values
    completion_tokens = response['usage']['completion_tokens']
    prompt_tokens = response['usage']['prompt_tokens']
    total_tokens = response['usage']['total_tokens']
    response_text = response['choices'][0]['message']['content']
    response_id = response['id']
    # Prepare the document to be stored
    document = {
        "id": unique_id,
        "timestamp": datetime.now().isoformat(),
        "chain_id":chain_id,
        "question_text": question_text,
        "question_id": question_id,
        "chat_id":chat_id,
        "user_id":user_id,
        "user_alias": user_alias,
        "user_location": user_location,
        "start_time": start_time,
        "media": media,
        "media_type": media_type,
        "start_time": start_time,
        "model":model,
        "role":"user",
        "max_token":max_token,
        "temperature": temperature,
        "token_used": total_tokens,
        "response_id":response_id,
        "response_text":response_text,
        "context_question":context_question
    }

    # Store the document in Azure Cosmos DB
    try:
        container.create_item(body=document)
        print("Chain Data stored successfully in Azure Cosmos DB.")
    except exceptions.CosmosHttpResponseError as e:
        print(f"An error occurred: {e.message}")



def insert_data_to_db_response(response, question_text, question_id, chat_id, user_id, user_alias, model):

    container = get_db_container("Response")
    # Extract the response values
    completion_tokens = response['usage']['completion_tokens']
    prompt_tokens = response['usage']['prompt_tokens']
    total_tokens = response['usage']['total_tokens']
    response_text = response['choices'][0]['message']['content']
    response_id = response['id']
    response_created_timestamp = response['created']
    response_created_datetime = datetime.fromtimestamp(response_created_timestamp).isoformat()


    # Generate a unique ID using UUID
    unique_id = str(uuid.uuid4())

    # Prepare the document to be stored
    document = {
        "id": unique_id,
        "timestamp": datetime.now().isoformat(),
        "question_text": question_text,
        "question_id": question_id,
        "chat_id":chat_id,
        "user_id":user_id,
        "user_alias": user_alias,
        "model":model,
        "role":"user",
        "token_used": total_tokens,
        "response_text": response_text,
        "response_id":response_id,
        "response_time":response_created_datetime
    }

    # Store the document in Azure Cosmos DB
    try:
        container.create_item(body=document)
        print("Response Data stored successfully in Azure Cosmos DB.")
    except exceptions.CosmosHttpResponseError as e:
        print(f"An error occurred: {e.message}")



def insert_data_to_db_related_question(question_text, question_id, chat_id, user_id, user_alias, user_location, start_time, media, media_type, model, temperature, max_token, related_question_list ,related_question_response):

    container = get_db_container("RelatedQuestion")
    # Extract the response values
    try:
        completion_tokens = related_question_response['usage']['completion_tokens']
        prompt_tokens = related_question_response['usage']['prompt_tokens']
        total_tokens = related_question_response['usage']['total_tokens']
        related_question_list = related_question_response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error extracting response values: {e}")
        completion_tokens = 0
        prompt_tokens = 0
        total_tokens = 0
        related_question_list = None

    # Generate a unique ID using UUID
    unique_id = str(uuid.uuid4())

    # Prepare the document to be stored
    document = {
        "id": unique_id,
        "timestamp": datetime.now().isoformat(),
        "question": question_text,
        "question_id": question_id,
        "chat_id":chat_id,
        "user_id":user_id,
        "user_alias": user_alias,
        "user_location": user_location,
        "start_time": start_time,
        "media": media,
        "media_type": media_type,
        "start_time": start_time,
        "model":model,
        "role":"user",
        "max_token":max_token,
        "temperature": temperature,
        "token_used": total_tokens,
        "related_question_text":related_question_list
    }

    # Store the document in Azure Cosmos DB
    try:
        container.create_item(body=document)
        print("Related Question Data stored successfully in Azure Cosmos DB.")
    except exceptions.CosmosHttpResponseError as e:
        print(f"An error occurred: {e.message}")




def check_is_question_related(new_question, previous_question, temperature, top_p, max_tokens):

    headers, ENDPOINT = get_chat_connection()
    conversation = [
    {"role": "user", "content": f"A user asked the following question: '{new_question}'"},
    {"role": "user", "content": f"Previously, they asked: '{previous_question}'"},
    {"role": "user", "content": "Is the new question related to the previous question? Please respond with 'yes' or 'no'."}
    ]
    payload = {
        "messages": conversation,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "stop": "exit"
    }

    try:
        print("HELLLOOO")
        # Send request
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Check for HTTP errors

        # Extract content
        response_json = response.json()
        message_content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        print("IS RELATED RESPONSE", response_json)
        print(message_content)
        # Check for 'yes' or 'no' answer in response content
        if message_content.lower() == 'yes' or message_content.lower()=='yes.':
            return True, response_json  # Related
        elif message_content.lower() == 'no' or message_content.lower()=='no.':
            return False, response_json  # Not related
        else:
            print("Unexpected response content:", message_content)
            return None

    except requests.RequestException as e:
        print(f"Failed to make the request. Error: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Failed to parse the response. Error: {e}")
        return None

def assign_chain_id(question_text, question_id, chat_id, user_id, start_time):
    # Fetch all previous questions and their chain IDs for the same chat_id
    all_question_list = fetch_user_chat_from_chat_id(chat_id)

    temperature = 0.7
    top_p = 0.95
    max_tokens = 800
    model = "gpt-4o"


    is_new_chain = True
    related_question_id = None
    related_question_text = None
    existing_chain_id = None
    response = None

    # Check if the new question is related to any previous questions
    if all_question_list:
        for question_data in all_question_list:
            previous_question_text = question_data["question_text"]
            chain_id = question_data["chain_id"]
            is_related, response = check_is_question_related(question_text, previous_question_text, temperature, top_p, max_tokens)
            # Use is_question_related to determine if the new question relates to previous ones
            if is_related:
                # If related, capture the chain_id and the related question details
                is_new_chain = False
                related_question_id = question_data["question_id"]
                related_question_text = previous_question_text
                existing_chain_id = chain_id
                break  # Exit the loop once a related question is found

    # Determine the chain_id to return
    chain_id_to_use = existing_chain_id if existing_chain_id else str(uuid.uuid4())

    # If this is a new chain, add to the database as needed here
    # For example, you could call insert_data_to_db_new_chain with this information
    print(chain_id_to_use)
    return chain_id_to_use, is_new_chain, temperature, top_p, max_tokens, response, {
        "related_question_id": related_question_id,
        "related_question_text": related_question_text,
        "all_question_list": all_question_list
    }




def find_similar_questions(new_question, temperature=0.7, top_p=0.95, max_tokens=50):
    """
    Find similar questions to a new question by calling the AI model.

    Parameters:
        new_question (str): The question for which we need to find similar questions.
        temperature (float): Sampling temperature for model response.
        top_p (float): Probability cutoff for nucleus sampling.
        max_tokens (int): Maximum tokens for response generation.

    Returns:
        list: List of questions suggested by the model as relevant or similar.
    """
    headers, ENDPOINT = get_chat_connection()

    # Prompt for AI to suggest similar questions
    conversation = [
        {"role": "user", "content": f"Here is a new question: '{new_question}'."},
        {"role": "user", "content": "Suggest similar questions that relate to the new question, please provide a list of suggestions."}
    ]
    payload = {
        "messages": conversation,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
    }

    try:
        # Send request to the model
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Ensure request was successful

        # Extract suggestions from response
        response_json = response.json()
        suggestions_text = response_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        # Split the suggestions into a list if the model returns multiple suggestions
        similar_questions = suggestions_text.split("\n") if suggestions_text else []
        return similar_questions, response_json

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except (KeyError, IndexError) as e:
        print(f"Failed to parse response: {e}")
        return []



def fetch_user_chat_from_chat_id(chat_id):
    container = get_db_container("Chain")

    # Fetch user chat from Azure Cosmos DB in descending order of timestamp
    user_chat_items = container.query_items(
        query = """
            SELECT c.question_id, c.question_text, c.chain_id
            FROM c
            WHERE c.chat_id = @chat_id AND IS_DEFINED(c.chain_id)
            ORDER BY c.timestamp DESC
        """,
        parameters=[{"name": "@chat_id", "value": chat_id}],
        enable_cross_partition_query=True
    )

    user_chat = []
    for item in user_chat_items:
        # Extract question_id, question_text, and chain_id for each entry
        user_chat.append({
            "question_id": item.get("question_id"),
            "question_text": item.get("question_text"),
            "chain_id": item.get("chain_id")
        })

    return user_chat



def fetch_user_chat_from_chain_id(chain_id):
    container = get_db_container("Chain")

    # Fetch user chat from Azure Cosmos DB
    user_chat_items = container.query_items(
        query=f"SELECT * FROM c WHERE c.chain_id = @chain_id",
        parameters=[{"name": "@chain_id", "value": chain_id}],
        enable_cross_partition_query=True
    )

    user_chat = []
    for item in user_chat_items:
        user_chat.append((item['question_text'], item['response_text']))  # Assuming both 'question' and 'response' are stored
    return user_chat
    
    
    
 