from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import json
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from sentence_transformers import SentenceTransformer
import torch

app = Flask(__name__, static_folder='../frontend/build/static', template_folder='../frontend/build')
CORS(app)  # Allow all origins for testing 

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
model = OllamaLLM(model="llama3.2")
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
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

# Route to handle user input and return bot response
@app.route('/submit', methods=['POST'])
def handle_data():
    # Receive JSON data
    data = request.get_json()
    user_input = data.get('userInput')
    conversation_history_json = data.get('history')
    
    if not user_input:
        return jsonify({"response": "Invalid input."}), 400

    # Parse conversation history with error handling
    try:
        conversation_history = json.loads(conversation_history_json) if conversation_history_json else []
    except json.JSONDecodeError:
        return jsonify({"response": "Invalid conversation history format."}), 400

    # Format the conversation history for the prompt
    formatted_history = ''
    for turn in conversation_history:
        role = 'User' if turn['role'] == 'user' else 'Assistant'
        formatted_history += f"{role}: {turn['content']}\n"

    # Get the relevant FAQs
    relevant_faqs = retrieve_faqs(user_input, faq_texts, faq_embeddings)

    # Get the response from the model
    result = prompt.format(faqs=relevant_faqs, question=user_input, history=formatted_history)
    assistant_response = model(result).strip()

    # Return the result as JSON
    return jsonify({"response": assistant_response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
