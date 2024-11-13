

# chat interface
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  

def load_faqs(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

json_path = 'fineTune/save.json'  
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
# model = OllamaLLM(model="llama3.2")
# model = OllamaLLM(model="llama3.2:1b")


prompt = ChatPromptTemplate.from_template(template)

# get relevance
def retrieve_faqs(question, faq_texts, faq_embeddings, k=3):
    # norma.ize embeddings
    question_embedding = embedding_model.encode(
        [question], convert_to_tensor=True, normalize_embeddings=True
    )
    # cosine similarities compare
    similarities = torch.matmul(faq_embeddings, question_embedding.T).squeeze()
    # get similar faqs
    top_k_indices = similarities.argsort(descending=True)[:k]
    relevant_faqs = [faq_texts[idx] for idx in top_k_indices]
    return '\n'.join(relevant_faqs)

# Route for the chat interface
@app.route('/')
def chat_interface():
    return render_template_string("""
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

    # parse conversation history
    conversation_history = json.loads(conversation_history_json) if conversation_history_json else []

    # format the conversation history for the prompt
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







# from flask import Flask, request, jsonify, render_template_string
# from flask_cors import CORS
# import json
# from langchain_ollama import OllamaLLM
# from langchain.prompts import ChatPromptTemplate
# from sentence_transformers import SentenceTransformer
# import torch

# app = Flask(__name__)
# CORS(app)

# def load_faqs(json_path):
#     with open(json_path, 'r', encoding='utf-8') as f:
#         return json.load(f)

# json_path = 'fineTune/data.json'
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

# Conversation history:
# {history}

# Here are some relevant FAQs:
# {faqs}

# Current question: {question}

# Answer (provide a brief and clear response):
# """

# # Create the model and prompt
# model = OllamaLLM(model="llama3.1")
# prompt = ChatPromptTemplate.from_template(template)

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

# # Route for the chat interface
# @app.route('/')
# def chat_interface():
#     # The main HTML file for the chat interface
#     return render_template_string("""
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>CoCo Assistant Chat</title>
#     <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
#     <link href="https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap" rel="stylesheet">
#     <style>
#         /* Your existing CSS styles */
#     </style>
# </head>
# <body>
#     <div class="chat-container">
#         <div id="chat-box" class="chat-box"></div>
#         <div class="input-container">
#             <input type="text" id="user-input" placeholder="Type a message..." onkeydown="if(event.key === 'Enter') sendMessage();">
#             <button onclick="sendMessage()">Send</button>
#         </div>
#     </div>

#     <script>
#         let conversationHistory = [];

#         function addMessage(content, className) {
#             const chatBox = document.getElementById('chat-box');
#             const messageContainer = document.createElement('div');
#             const message = document.createElement('div');
#             message.className = 'chat-message ' + className;
#             message.innerText = content;
#             messageContainer.appendChild(message);
#             chatBox.appendChild(messageContainer);
#             chatBox.scrollTop = chatBox.scrollHeight;
#         }

#         async function sendMessage() {
#             const userInput = document.getElementById('user-input');
#             const message = userInput.value;
#             if (!message.trim()) return;

#             // Display user message in chat box
#             addMessage(message, 'user-message');
#             conversationHistory.push({'role': 'user', 'content': message});
#             userInput.value = '';

#             try {
#                 // Prepare form data
#                 const formData = new FormData();
#                 formData.append('userInput', message);
#                 formData.append('history', JSON.stringify(conversationHistory));

#                 // Send message to the server
#                 const response = await fetch('/submit', {
#                     method: 'POST',
#                     body: formData
#                 });

#                 const data = await response.json();

#                 // Display bot response in chat box
#                 addMessage(data.response, 'bot-message');
#                 conversationHistory.push({'role': 'assistant', 'content': data.response});
#             } catch (error) {
#                 console.error('Error:', error);
#                 addMessage('An error occurred while sending your message.', 'bot-message');
#             }
#         }

#         // Function to programmatically trigger sending message
#         function triggerSendMessage() {
#             sendMessage();
#         }
#     </script>
# </body>
# </html>
#     """)

# # Route to handle user input and return bot response
# @app.route('/submit', methods=['POST'])
# def handle_data():
#     # Log the request headers for debugging
#     print("Headers:", request.headers)
#     print("Content-Type:", request.content_type)

#     # Get data from form
#     user_input = request.form.get('userInput')
#     conversation_history_json = request.form.get('history')

#     if not user_input:
#         return jsonify({"response": "Invalid input."}), 400

#     # Parse conversation history
#     conversation_history = json.loads(conversation_history_json) if conversation_history_json else []

#     # Format the conversation history for the prompt
#     formatted_history = ''
#     for turn in conversation_history:
#         role = 'User' if turn['role'] == 'user' else 'Assistant'
#         formatted_history += f"{role}: {turn['content']}\n"

#     # Get the relevant FAQs
#     relevant_faqs = retrieve_faqs(user_input, faq_texts, faq_embeddings)

#     # Get the response from the chain
#     result = prompt.format(faqs=relevant_faqs, question=user_input, history=formatted_history)
#     assistant_response = model(result).strip()

#     # Return the result as JSON
#     return jsonify({"response": assistant_response})

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8080)
