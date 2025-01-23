import os


def get_chat_connection():
    API_KEY = os.getenv("API_KEY", "23nQHUkVJwa1sO5S25vkVyFWc1guCgrWQGjlhmknyex0k37JYb28JQQJ99AJACYeBjFXJ3w3AAABACOGUXD0")
    ENDPOINT = os.getenv("API_ENDPOINT", "https://phnkai-10.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview")

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    return headers, ENDPOINT