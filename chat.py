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
    context = ""
    print("Welcome to the AI Chatbot, type exit to quit")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        relevant_faqs = retrieve_faqs(user_input, faqs)

        result = chain.invoke({"faqs": relevant_faqs, "question": user_input})
        print("Coco: ", result, "\n")
        # context += f"\nUser: {user_input}\nAI: {result}"


# Function to access the JSON file containing all frequently asked questions and answers
def retrieve_faqs(question, faqs):
    keywords = question.lower().split()
    relevant_faqs = []

    # Search through JSON data
    for faq in faqs:
        if any(keyword in faq['prompt'].lower() for keyword in keywords):
            relevant_faqs.append(f"**Question:** {faq['prompt']}\n**Answer:** {faq['completion']}")
    
    return '\n'.join(relevant_faqs)


# Testing function to see if the JSON file works
# def test_json_loading(faqs):
#     # Print the entire JSON data (be careful with large data)
#     print("Loaded JSON Data:")
#     print(json.dumps(faqs, indent=4))  # Pretty-print the JSON data

#     # Check the type of the loaded data
#     print("\nType of loaded data:", type(faqs))

#     # Check the length (number of entries)
#     print("Number of FAQs loaded:", len(faqs))

#     # Check the structure of the first entry (if it exists)
#     if faqs:
#         print("\nFirst FAQ entry structure:")
#         print("Prompt:", faqs[0].get("prompt"))
#         print("Completion:", faqs[0].get("completion"))
#         print("Tags:", faqs[0].get("tags"))


if __name__ == "__main__":
    json_path = 'fineTune/data.json'
    faqs = load_faqs(json_path)


    handle_conversation(faqs)


    # Testing call
    # test_json_loading(faqs)


