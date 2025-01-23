from flask import jsonify

def create_response(status_code, message, data=None):
    """
    Creates a JSON response with a status code, message, and optional data.
    """
    response = {
        "status_code": status_code,
        "message": message,
        "data": data if data is not None else {}
    }
    return jsonify(response), status_code
