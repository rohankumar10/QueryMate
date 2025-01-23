import os

class Config:
    API_KEY = os.getenv("API_KEY")
    API_ENDPOINT = os.getenv("API_ENDPOINT")
    COSMOS_ENDPOINT = os.getenv("COMOS_ENDPOINT")
    COSMOS_KEY = os.getenv("COSMOS_KEY")
    GLOBAL_TEMPERATURE = 0.7
    GLOBAL_TOP_P = 0.95
    GLOBAL_MAX_TOKENS = 800
    GLOBAL_MODEL = "gpt-4o"
