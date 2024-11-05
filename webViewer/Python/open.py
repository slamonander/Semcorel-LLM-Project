from flask import Flask, request
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)  # This enables CORS on all routes

# Get the OpenAI API key from an environment variable
OPENAI_API_KEY = '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'
if not OPENAI_API_KEY:
    raise Exception("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

def llama3(prompt):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}',
    }
    data = {
        'model': 'gpt-3.5-turbo',  # or 'gpt-4' if you have access
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.7,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            json_response = response.json()
            # Adjust parsing based on actual response
            if 'choices' in json_response:
                return json_response['choices'][0]['message']['content']
            else:
                return f"Unexpected response structure: {json_response}"
        except (json.JSONDecodeError, KeyError) as e:
            return f"Failed to parse JSON response: {e}"
    else:
        try:
            error_response = response.json()
            return f"API Error: {error_response.get('error', {}).get('message', 'Unknown error')}"
        except json.JSONDecodeError:
            return f"Request failed with status code {response.status_code}: {response.text}"

@app.route('/submit', methods=['POST'])
def handle_data():
    user_input = request.form['userInput']
    with open('received_data.txt', 'a') as file:
        file.write(user_input + '\n')
    
    # Get the response from OpenAI API
    openai_response = llama3(user_input)
    
    # Return the response to the user
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
            {openai_response}
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)


