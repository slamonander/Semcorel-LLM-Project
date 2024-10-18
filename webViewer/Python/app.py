# from flask import Flask, request
# from flask_cors import CORS
# app = Flask(__name__)
# CORS(app)  # This enables CORS on all routes

# @app.route('/submit', methods=['POST'])
# def handle_data():
#     user_input = request.form['userInput']
#     with open('received_data.txt', 'a') as file:
#         file.write(user_input + '\n')
#     # this return statement is technically a html file
#     return f"<h1> Received and saved: {user_input} </h1>"

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')  

from flask import Flask, request
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # This enables CORS on all routes

# Llama API URL
url = "http://localhost:11434/api/chat"

def llama3(prompt):
    data = {
        "model": "Llama3.1",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        try:
            json_response = response.json()
            print("Raw response JSON:", json.dumps(json_response, indent=2))
            # Adjust parsing based on actual response
            if 'choices' in json_response:
                return json_response['choices'][0]['message']['content']
            elif 'message' in json_response:
                return json_response['message']['content']
            else:
                return f"Unexpected response structure: {json_response}"
        except (json.JSONDecodeError, KeyError) as e:
            return f"Failed to parse JSON response: {e}"
    else:
        try:
            error_response = response.json()
            return f"API Error: {error_response.get('error', 'Unknown error')}"
        except json.JSONDecodeError:
            return f"Request failed with status code {response.status_code}: {response.text}"


@app.route('/submit', methods=['POST'])
def handle_data():
    user_input = request.form['userInput']
    with open('received_data.txt', 'a') as file:
        file.write(user_input + '\n')
    
    # Get the response from Llama
    llama_response = llama3(user_input)
    
    # Return the Llama response to the user
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background-color: #f5f5f5;
            }}
            .response {{
                max-width: 600px;
                width: 90%;
                background-color: #ffffff;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                font-size: 1.2em;
                color: #333;
                text-align: center;
                line-height: 1.5;
            }}
        </style>
    </head>
    <body>
        <div class="response">
            {llama_response}
        </div>
    </body>
    </html>
    """


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

