import json
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

#load in the dictionary of functions.
#the dictionary contains pointers so we can really call any function.
import flask_connector_settings
functions_dictionary = flask_connector_settings.functions_dictionary




app = Flask(__name__)
CORS(app)

def check_for_JSON():
    """Validates whether the request body contains a JSON-like string and converts it into a structured JSON response."""
    response = None  # Initialize response variable

    # Checking if request body is a JSON-like string by attempting to convert it from a string to a dictionary
    try:  
        request_body = request.data.decode('utf-8')  # Convert raw bytes to a string representation
        json_data = json.loads(request_body)  # Try to convert the string into a Python dictionary (structured data)
        print("\n--- JSON Check ---\nExtracted JSON-like string:\n", json_data)  # Debugging output

        json_string = json.dumps(json_data)  # Convert dictionary back into a proper JSON-formatted string
        response = make_response(json_string)
        response.status_code = 200  # OK
        response.headers["Content-Type"] = "application/json"
    
    # Handling cases where request body is not a JSON-like string and cannot be converted
    except json.JSONDecodeError:  
        print("\n--- JSON Check ---\nError: Request body is not a valid JSON-like string.\n")
        response = make_response(jsonify({"error": "Request contains a JSON-like string that could not be properly parsed"}))
        response.status_code = 400  # Bad Request

    return response  

@app.route('/', defaults={'path': ''}, methods=["GET", "OPTIONS", "POST"])
@app.route('/<path:path>', methods=["GET", "OPTIONS", "POST"])
def handle_request(path):
    # Log request details
    print("\n##### NEW REQUEST #####\n")
    print("\n--- Request Details ---")
    print(f"Received request at path: /{path}")
    print(f"Request method: {request.method}\n")

    # Print request headers
    print("\n--- Request Headers ---")
    for header, value in request.headers.items():
        print(f"{header}: {value}")
    print("\n")

    # Print request body
    request_body = request.data.decode('utf-8') if request.data else ""
    print(f"\n--- Request Body ---\n{request_body if request_body else 'No body content'}\n")

    # Properly initialized response variable
    response = make_response("")  # Empty response to avoid unnecessary processing

    if request.method == "OPTIONS":
        response.status_code = 204  # No Content
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS, POST"
        response.headers["Access-Control-Allow-Headers"] = "*"
    elif request.method == "POST":
        #This is the section of code that does the function call.
        #The request body must be a JSON-like string with field simulate, and field within that called "simulation_function_label"
        #the "simulation_function_label" must be assigned to the desired function in 
        response = check_for_JSON()  # Process JSON validation
        json_data = json.loads(request_body)
        if 'simulate' in json_data:
            simulation_function_name = json_data['simulate']["simulation_function_label"]
        else:
            simulation_function_name = ''
            response.status_code = 400  # Bad Request
        function_chosen = functions_dictionary[simulation_function_name]
        simulation_output = function_chosen(json_data)
        #just do a back and forth conversion to make sure JSON-like string is okay.

        # Ensure the input is valid json by converting it back and forth to a string.
        try:
            json_string = json.dumps(simulation_output)
            json_dict = json.loads(json_string)
        except:
            raise TypeError("Output from simulation function cannnot be converted to JSON.")
        response.set_data(json_dict)
    elif request.method == "GET":
        response = make_response("Hello, World!")
        response.status_code = 200  # OK

    # Log response headers
    print("\n--- Response Headers ---")
    for header, value in response.headers.items():
        print(f"{header}: {value}")
    print("\n")

    if request.method == "POST":
        response = json_dict
    return response  # Always return a response variable

# Allow all origins dynamically
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
