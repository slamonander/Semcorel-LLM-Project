# # from flask import Flask, request
# # from flask_cors import CORS
# # app = Flask(__name__)
# # CORS(app)  # This enables CORS on all routes

# # @app.route('/submit', methods=['POST'])
# # def handle_data():
# #     user_input = request.form['userInput']
# #     with open('received_data.txt', 'a') as file:
# #         file.write(user_input + '\n')
# #     # this return statement is technically a html file
# #     return f"<h1> Received and saved: {user_input} </h1>"

# # if __name__ == '__main__':
# #     app.run(debug=True, host='0.0.0.0')  

# from flask import Flask, request
# from flask_cors import CORS
# import requests
# import json

# app = Flask(__name__)
# CORS(app)  # This enables CORS on all routes

# url = "http://localhost:11434/api/chat"

# def llama3(prompt):
#     data = {
#         "model": "Llama3.2",
#         # "model": "Llama3.2:1b",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         "stream": False
#     }

#     headers = {
#         "Content-Type": "application/json"
#     }

#     response = requests.post(url, headers=headers, json=data)
    
#     if response.status_code == 200:
#         try:
#             json_response = response.json()
#             print("Raw response JSON:", json.dumps(json_response, indent=2))
#             # Adjust parsing based on actual response
#             if 'choices' in json_response:
#                 return json_response['choices'][0]['message']['content']
#             elif 'message' in json_response:
#                 return json_response['message']['content']
#             else:
#                 return f"Unexpected response structure: {json_response}"
#         except (json.JSONDecodeError, KeyError) as e:
#             return f"Failed to parse JSON response: {e}"
#     else:
#         try:
#             error_response = response.json()
#             return f"API Error: {error_response.get('error', 'Unknown error')}"
#         except json.JSONDecodeError:
#             return f"Request failed with status code {response.status_code}: {response.text}"


# @app.route('/submit', methods=['POST'])
# def handle_data():
#     user_input = request.form['userInput']
#     with open('received_data.txt', 'a') as file:
#         file.write(user_input + '\n')
    
#     # Get the response from Llama
#     llama_response = llama3(user_input)
    
#     # Return the Llama response to the user
#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 padding: 20px;
#                 margin: 0;
#                 display: flex;
#                 justify-content: center;
#                 align-items: center;
#                 min-height: 100vh;
#                 background-color: #f5f5f5;
#             }}
#             .response {{
#                 max-width: 600px;
#                 width: 90%;
#                 background-color: #ffffff;
#                 padding: 15px;
#                 border-radius: 10px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
#                 font-size: 1.2em;
#                 color: #333;
#                 text-align: center;
#                 line-height: 1.5;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="response">
#             {llama_response}
#         </div>
#     </body>
#     </html>
#     """


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8080)



# from flask import Flask, request
# from flask_cors import CORS
# import json
# from langchain_ollama import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate

# app = Flask(__name__)
# CORS(app)  # This enables CORS on all routes

# # Load FAQs from JSON
# def load_faqs(json_path):
#     with open(json_path, 'r') as f:
#         return json.load(f)

# # Load FAQs
# json_path = 'fineTune/data.json'  # Update this path to your JSON file location
# faqs = load_faqs(json_path)

# # Define the template
# template = """
# Answer the question below. You are a customer service bot working for a company called SemCorel.

# Here are some relevant FAQs:
# {faqs}

# Question: {question}

# Answer:
# """

# # Create the model, prompt, and chain
# model = OllamaLLM(model="llama3.1")
# prompt = ChatPromptTemplate.from_template(template)
# chain = prompt | model

# # Function to retrieve relevant FAQs
# def retrieve_faqs(question, faqs):
#     keywords = question.lower().split()
#     relevant_faqs = []

#     # Search through JSON data
#     for faq in faqs:
#         if any(keyword in faq['prompt'].lower() for keyword in keywords):
#             relevant_faqs.append(f"**Question:** {faq['prompt']}\n**Answer:** {faq['completion']}")
    
#     return '\n'.join(relevant_faqs)

# @app.route('/submit', methods=['POST'])
# def handle_data():
#     user_input = request.form['userInput']
#     with open('received_data.txt', 'a') as file:
#         file.write(user_input + '\n')

#     # Get the relevant FAQs
#     relevant_faqs = retrieve_faqs(user_input, faqs)

#     # Get the response from the chain
#     result = chain.invoke({"faqs": relevant_faqs, "question": user_input})

#     # Return the result as HTML
#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 padding: 20px;
#                 margin: 0;
#                 display: flex;
#                 justify-content: center;
#                 align-items: center;
#                 min-height: 100vh;
#                 background-color: #f5f5f5;
#             }}
#             .response {{
#                 max-width: 600px;
#                 width: 90%;
#                 background-color: #ffffff;
#                 padding: 15px;
#                 border-radius: 10px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
#                 font-size: 1.2em;
#                 color: #333;
#                 text-align: center;
#                 line-height: 1.5;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="response">
#             {result}
#         </div>
#     </body>
#     </html>
#     """

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8080)




# code with fetching

# from flask import Flask, request
# from flask_cors import CORS
# import json
# from langchain_ollama import OllamaLLM
# from langchain.prompts import ChatPromptTemplate
# from sentence_transformers import SentenceTransformer
# import numpy as np

# app = Flask(__name__)
# CORS(app)  # This enables CORS on all routes

# # Load FAQs from JSON
# def load_faqs(json_path):
#     with open(json_path, 'r', encoding='utf-8') as f:
#         return json.load(f)

# # Load FAQs
# json_path = 'fineTune/data.json'  # Update this path to your JSON file location
# faqs = load_faqs(json_path)

# # Create a list of FAQ documents
# faq_texts = [f"Question: {faq['prompt']}\nAnswer: {faq['completion']}" for faq in faqs]

# # Initialize the local embeddings model
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Runs locally
# faq_embeddings = embedding_model.encode(faq_texts, convert_to_tensor=True)

# # Define the template with instructions for conciseness
# template = """
# You are a helpful customer service assistant for a company called SemCorel. Answer the user's question concisely and clearly.

# Here are some relevant FAQs:
# {faqs}

# Question: {question}

# Answer (provide a brief and clear response):
# """

# # Create the model, prompt, and chain
# model = OllamaLLM(model="llama3.1")
# prompt = ChatPromptTemplate.from_template(template)
# chain = prompt | model

# # Function to retrieve the most relevant FAQs
# def retrieve_faqs(question, faq_texts, faq_embeddings, k=3):
#     question_embedding = embedding_model.encode([question], convert_to_tensor=True)
#     # Compute cosine similarities
#     similarities = (faq_embeddings @ question_embedding.T).squeeze()
#     # Get the top k most similar FAQs
#     top_k_indices = similarities.argsort(descending=True)[:k]
#     relevant_faqs = [faq_texts[idx] for idx in top_k_indices]
#     return '\n'.join(relevant_faqs)

# @app.route('/submit', methods=['POST'])
# def handle_data():
#     user_input = request.form['userInput']
#     with open('received_data.txt', 'a', encoding='utf-8') as file:
#         file.write(user_input + '\n')

#     # Get the relevant FAQs
#     relevant_faqs = retrieve_faqs(user_input, faq_texts, faq_embeddings)

#     # Get the response from the chain
#     result = chain.invoke({"faqs": relevant_faqs, "question": user_input})

#     # Return the result as HTML
#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 padding: 20px;
#                 margin: 0;
#                 display: flex;
#                 justify-content: center;
#                 align-items: center;
#                 min-height: 100vh;
#                 background-color: #f5f5f5;
#             }}
#             .response {{
#                 max-width: 600px;
#                 width: 90%;
#                 background-color: #ffffff;
#                 padding: 15px;
#                 border-radius: 10px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
#                 font-size: 1.2em;
#                 color: #333;
#                 text-align: center;
#                 line-height: 1.5;
#                 white-space: pre-wrap;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="response">
#             {result.strip()}
#         </div>
#     </body>
#     </html>
#     """

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8080)


# newcode


# from flask import Flask, request
# from flask_cors import CORS
# import json
# from langchain_ollama import OllamaLLM
# from langchain.prompts import ChatPromptTemplate
# from sentence_transformers import SentenceTransformer
# import torch

# app = Flask(__name__)
# CORS(app)  # This enables CORS on all routes

# # Load FAQs from JSON
# def load_faqs(json_path):
#     with open(json_path, 'r', encoding='utf-8') as f:
#         return json.load(f)

# # Load FAQs
# json_path = 'fineTune/data.json'  # Update this path to your JSON file location
# faqs = load_faqs(json_path)

# # Create a list of FAQ documents
# faq_texts = [f"Question: {faq['prompt']}\nAnswer: {faq['completion']}" for faq in faqs]

# # Initialize the local embeddings model
# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Runs locally

# # Load and normalize FAQ embeddings
# faq_embeddings = embedding_model.encode(
#     faq_texts, convert_to_tensor=True, normalize_embeddings=True
# )

# # Define the template with instructions for conciseness
# template = """
# You are a helpful customer service assistant for a company called SemCorel. Answer the user's question concisely and clearly.

# Here are some relevant FAQs:
# {faqs}

# Question: {question}

# Answer (provide a brief and clear response):
# """

# # Create the model, prompt, and chain
# model = OllamaLLM(model="llama3.1")
# prompt = ChatPromptTemplate.from_template(template)
# chain = prompt | model

# # Function to retrieve the most relevant FAQs
# def retrieve_faqs(question, faq_texts, faq_embeddings, k=3):
#     # Normalize the question embedding
#     question_embedding = embedding_model.encode(
#         [question], convert_to_tensor=True, normalize_embeddings=True
#     )
#     # Compute cosine similarities
#     similarities = torch.matmul(faq_embeddings, question_embedding.T).squeeze()
#     # Get the top k most similar FAQs
#     top_k_indices = similarities.argsort(descending=True)[:k]
#     relevant_faqs = [faq_texts[idx] for idx in top_k_indices]
#     return '\n'.join(relevant_faqs)

# @app.route('/submit', methods=['POST'])
# def handle_data():
#     user_input = request.form['userInput']
#     with open('received_data.txt', 'a', encoding='utf-8') as file:
#         file.write(user_input + '\n')

#     # Get the relevant FAQs
#     relevant_faqs = retrieve_faqs(user_input, faq_texts, faq_embeddings)

#     # Get the response from the chain
#     result = chain.invoke({"faqs": relevant_faqs, "question": user_input})

#     # Return the result as HTML
#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 padding: 20px;
#                 margin: 0;
#                 display: flex;
#                 justify-content: center;
#                 align-items: center;
#                 min-height: 100vh;
#                 background-color: #f5f5f5;
#             }}
#             .response {{
#                 max-width: 600px;
#                 width: 90%;
#                 background-color: #ffffff;
#                 padding: 15px;
#                 border-radius: 10px;
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
#                 font-size: 1.2em;
#                 color: #333;
#                 text-align: center;
#                 line-height: 1.5;
#                 white-space: pre-wrap;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="response">
#             {result.strip()}
#         </div>
#     </body>
#     </html>
#     """

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8080)


# chat interface
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from sentence_transformers import SentenceTransformer
import torch

app = Flask(__name__)
CORS(app)  

def load_faqs(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

json_path = 'fineTune/data.json'  
faqs = load_faqs(json_path)

# Create a list of FAQ documents
faq_texts = [f"Question: {faq['prompt']}\nAnswer: {faq['completion']}" for faq in faqs]

# Initialize the local embeddings model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Runs locally

# Load and normalize FAQ embeddings
faq_embeddings = embedding_model.encode(
    faq_texts, convert_to_tensor=True, normalize_embeddings=True
)

# Define the template with instructions for conciseness
template = """
You are a helpful customer service assistant for a company called SemCorel. Answer the user's question concisely and clearly.

Conversation history:
{history}

Here are some relevant FAQs:
{faqs}

Current question: {question}

Answer (provide a brief and clear response):
"""

# Create the model and prompt
model = OllamaLLM(model="llama3.1")
prompt = ChatPromptTemplate.from_template(template)

# Function to retrieve the most relevant FAQs
def retrieve_faqs(question, faq_texts, faq_embeddings, k=3):
    # Normalize the question embedding
    question_embedding = embedding_model.encode(
        [question], convert_to_tensor=True, normalize_embeddings=True
    )
    # Compute cosine similarities
    similarities = torch.matmul(faq_embeddings, question_embedding.T).squeeze()
    # Get the top k most similar FAQs
    top_k_indices = similarities.argsort(descending=True)[:k]
    relevant_faqs = [faq_texts[idx] for idx in top_k_indices]
    return '\n'.join(relevant_faqs)

# Route for the chat interface
@app.route('/')
def chat_interface():
    # The main HTML file for the chat interface
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>CoCo Assistant Chat</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <link href="https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(135deg, #e2ebf0, #cfd9e2);
                margin: 0;
                flex-direction: column;
                padding: 0 15px;
                box-sizing: border-box;
            }
            .chat-container {
                width: 100%;
                max-width: 600px;
                background: #ffffff;
                padding: 20px;
                border-radius: 20px;
                box-shadow: 0px 15px 25px rgba(0, 0, 0, 0.2);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                border: 2px solid #007bff;
                height: 80vh;
                max-height: 700px;
            }
            .chat-box {
                flex-grow: 1;
                overflow-y: auto;
                margin-bottom: 15px;
                padding-right: 10px;
                display: flex;
                flex-direction: column;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
                background: #f3f4f6;
                max-height: calc(100% - 100px);
            }
            .chat-message {
                padding: 15px;
                border-radius: 25px;
                margin: 10px 0;
                max-width: 75%;
                word-wrap: break-word;
                display: inline-block;
                font-size: 16px;
            }
            .user-message {
                background: linear-gradient(135deg, #007bff, #0056b3);
                color: #fff;
                align-self: flex-end;
                border-bottom-right-radius: 5px;
                animation: slide-in 0.5s ease-out;
                text-align: right;
            }
            .bot-message {
                background: #e0e0e0;
                color: #333;
                align-self: flex-start;
                border-bottom-left-radius: 5px;
                animation: slide-in 0.5s ease-out;
                text-align: left;
            }
            .input-container {
                display: flex;
                align-items: center;
                margin-top: 10px;
                padding: 10px;
                border-radius: 10px;
                background: #ffffff;
                box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
            }
            input[type="text"] {
                flex-grow: 1;
                padding: 15px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 15px;
                margin-right: 10px;
                outline: none;
                transition: all 0.3s ease;
            }
            input[type="text"]:focus {
                border-color: #007bff;
                box-shadow: 0px 0px 5px rgba(0, 123, 255, 0.5);
            }
            button {
                padding: 15px 25px;
                font-size: 16px;
                color: #fff;
                background: linear-gradient(135deg, #007bff, #0056b3);
                border: none;
                border-radius: 15px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #004080;
            }
            @keyframes slide-in {
                0% {
                    transform: translateY(30px);
                    opacity: 0;
                }
                100% {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div id="chat-box" class="chat-box"></div>
            <div class="input-container">
                <input type="text" id="user-input" placeholder="Type a message..." onkeydown="if(event.key === 'Enter') sendMessage();">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            let conversationHistory = [];

            function addMessage(content, className) {
                const chatBox = document.getElementById('chat-box');
                const messageContainer = document.createElement('div');
                const message = document.createElement('div');
                message.className = 'chat-message ' + className;
                message.innerText = content;
                messageContainer.appendChild(message);
                chatBox.appendChild(messageContainer);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            async function sendMessage() {
                const userInput = document.getElementById('user-input');
                const message = userInput.value;
                if (!message.trim()) return;
                
                // Display user message in chat box
                addMessage(message, 'user-message');
                conversationHistory.push({'role': 'user', 'content': message});
                userInput.value = '';

                try {
                    // Prepare form data
                    const formData = new FormData();
                    formData.append('userInput', message);
                    formData.append('history', JSON.stringify(conversationHistory));

                    // Send message to the server
                    const response = await fetch('/submit', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    // Display bot response in chat box
                    addMessage(data.response, 'bot-message');
                    conversationHistory.push({'role': 'assistant', 'content': data.response});
                } catch (error) {
                    console.error('Error:', error);
                    addMessage('An error occurred while sending your message.', 'bot-message');
                }
            }
        </script>
    </body>
    </html>
    """)

# Route to handle user input and return bot response
@app.route('/submit', methods=['POST'])
def handle_data():
    # Log the request headers for debugging
    print("Headers:", request.headers)
    print("Content-Type:", request.content_type)

    # Get data from form
    user_input = request.form.get('userInput')
    conversation_history_json = request.form.get('history')

    if not user_input:
        return jsonify({"response": "Invalid input."}), 400

    # Parse conversation history
    conversation_history = json.loads(conversation_history_json) if conversation_history_json else []

    # Format the conversation history for the prompt
    formatted_history = ''
    for turn in conversation_history:
        role = 'User' if turn['role'] == 'user' else 'Assistant'
        formatted_history += f"{role}: {turn['content']}\n"

    # Get the relevant FAQs
    relevant_faqs = retrieve_faqs(user_input, faq_texts, faq_embeddings)

    # Get the response from the chain
    result = prompt.format(faqs=relevant_faqs, question=user_input, history=formatted_history)
    assistant_response = model(result).strip()

    # Return the result as JSON
    return jsonify({"response": assistant_response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
