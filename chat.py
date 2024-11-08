from tts import speak
from stt import speech_to_text


from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
# from reader import extract_text
import json

# Load FAQs from JSON
def load_faqs(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)



# Template for the conversation and initializing the model, prompt, and chain
template = """
Answer the question below. You are a customer service bot working for a company called SemCorel.

Here are some relevant FAQs:
{faqs}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model 


# Function that handles the conversation between user and model
def handle_conversation(faqs):
    # context = ""

    print("Welcome to the AI Chatbot, type exit to quit")


    while True:
        tts = input("If you would like TTS, type TTS.").strip().lower()
        stt = input("Type T for text input or V for voice input: ").strip().lower()

        if stt == 't':
            user_input = input("You: ")
        elif stt == 'v':
            user_input = speech_to_text()
            if user_input is None:
                continue
        else:
            print("Please type in 'T' for text and 'V' for voice.")
            continue


        if user_input.lower() == "exit":
            break


        relevant_faqs = retrieve_faqs(user_input, faqs)

        result = chain.invoke({"faqs": relevant_faqs, "question": user_input}) # Clear this up
        print("Coco: ", result, "\n")
        # context += f"\nUser: {user_input}\nAI: {result}"

        # If TTS is selected:
        if tts == 'tts':
            speak(result)






# Function to access the JSON file containing all frequently asked questions and answers
def retrieve_faqs(question, faqs):
    keywords = question.lower().split()
    relevant_faqs = []

    # Search through JSON data
    for faq in faqs:
        if any(keyword in faq['Prompts'].lower() for keyword in keywords):
            relevant_faqs.append("Question: {faq['Prompts']}\nAnswer: {faq['Completion']}")
    
    return '\n'.join(relevant_faqs)



if __name__ == "__main__":
    json_path = 'fineTune/data.json'
    faqs = load_faqs(json_path)


    handle_conversation(faqs)




