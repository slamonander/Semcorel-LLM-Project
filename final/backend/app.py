from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import json
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from sentence_transformers import SentenceTransformer
from stt import speech_to_text
import re
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
You are a helpful customer service assistant for a company called SemCorel. Answer the user's question concisely and clearly. You are only allowed to answer questions related to SemCorel's technical support. 
If the user's question is not related to SemCorel or is unclear, politely inform them that you cannot assist with unrelated matters.

Conversation history:
{history}

Here are some relevant FAQs:
{faqs}

Current question: {question}

Answer (provide a brief and clear response, respond only if the question is related to SemCorel's technical support):
"""

# Create the model and prompt
# model = OllamaLLM(model="llama3.2-vision")
model = OllamaLLM(model="llama3.2")

prompt = ChatPromptTemplate.from_template(template)

# Function to retrieve the most relevant FAQs
# Function to format FAQs into a clear bullet point list
def format_faq_answer(answer):
    # Use a regular expression to insert line breaks before each numbered point
    formatted_answer = re.sub(r"(?<!\n)(\d\.\s)", r"\n\1", answer).strip()
    return formatted_answer

def retrieve_faqs(question, faq_texts, faq_embeddings, k=3):
    try:
        question_embedding = embedding_model.encode(
            [question], convert_to_tensor=True, normalize_embeddings=True
        )
        similarities = torch.matmul(faq_embeddings, question_embedding.T).squeeze()
        top_k_indices = similarities.argsort(descending=True)[:k]
        relevant_faqs = [faq_texts[idx] for idx in top_k_indices]
        
        if relevant_faqs:
            # Format the FAQ answers for better readability
            formatted_faqs = "\n".join(
                f"Question: {faq.split('Answer:')[0].strip()}\n"
                f"Answer: {format_faq_answer(faq.split('Answer:')[1].strip())}"
                for faq in relevant_faqs
            )
            return formatted_faqs
        else:
            return "No FAQs found."
    except Exception as e:
        print(f"Error retrieving FAQs: {e}")
        return "Error retrieving FAQs."


# Route for the chat interface
@app.route('/')
def chat_interface():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

# BONUS FEATURE ROUTING
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_endpoint():
    result = speech_to_text()
    if result["success"]:
        transcription = result["transcription"]
        return jsonify({"transcription": transcription}), 200
    else:
        return jsonify({"error": result["error"]}), 400


@app.route('/process-speech', methods=['POST'])
def process_speech():
    data = request.get_json()
    transcription = data.get('transcript')  # Use the frontend's transcript

    if not transcription:
        return jsonify({"error": "No transcription provided."}), 400

    # Retrieve LLM response using the existing logic
    formatted_history = ''  # Use an empty history for now
    relevant_faqs = retrieve_faqs(transcription, faq_texts, faq_embeddings)
    result = prompt.format(faqs=relevant_faqs, question=transcription, history=formatted_history)
    assistant_response = model(result).strip()

    return jsonify({
        "transcription": transcription,
        "response": assistant_response
    }), 200



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

    # Apply formatting to ensure proper line breaks
    formatted_response = format_faq_answer(assistant_response)

    # Return the formatted result as JSON
    return jsonify({"response": formatted_response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)