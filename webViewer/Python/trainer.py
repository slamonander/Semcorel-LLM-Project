import streamlit as st


import os
import time


#userprompt
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


#vectorDB
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings


#llms
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager


#pdf loader
from langchain_community.document_loaders import PyPDFLoader


#pdf processing
from langchain.text_splitter import RecursiveCharacterTextSplitter


#retrieval
from langchain.chains import RetrievalQA


if not os.path.exists('pdfFiles'):
   os.makedirs('pdfFiles')


if not os.path.exists('vectorDB'):
   os.makedirs('vectorDB')




if 'template' not in st.session_state:
   st.session_state.template = """You are a knowledgeable chatbot, here to help with questions of the user. Your tone should be professional and informative.


   Context: {context}
   History: {history}


   User: {question}
   Chatbot:"""


if 'prompt' not in st.session_state:
   st.session_state.prompt = PromptTemplate(
       input_variables=["history", "context", "question"],
       template=st.session_state.template,
   )


if 'memory' not in st.session_state:
   st.session_state.memory = ConversationBufferMemory(
       memory_key="history",
       return_messages=True,
       input_key="question",
   )


if 'vectorstore' not in st.session_state:
   st.session_state.vectorstore = Chroma(persist_directory='vectorDb',
                                           embedding_function=OllamaEmbeddings(base_url='http://localhost:11434',
                                           model="llama3.1")
                                           )
  
if 'llm' not in st.session_state:
   st.session_state.llm = Ollama(base_url="http://localhost:11434",
                                 model="llama3.1",
                                 verbose=True,
                                 callback_manager=CallbackManager(
                                     [StreamingStdOutCallbackHandler()]),
                                 )
  
if 'chat_history' not in st.session_state:
   st.session_state.chat_history = []


st.title("Chatbot - to talk to PDFs")


uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")


for message in st.session_state.chat_history:
   with st.chat_message(message["role"]):
       st.markdown(message["message"])


if uploaded_file is not None:
   st.text("File uploaded successfully")
   if not os.path.exists('pdfFiles/' + uploaded_file.name):
       with st.status("Saving file..."):
           bytes_data = uploaded_file.read()
           f = open('pdfFiles/' + uploaded_file.name, 'wb')
           f.write(bytes_data)
           f.close()


           loader = PyPDFLoader('pdfFiles/' + uploaded_file.name)
           data = loader.load()


           text_splitter = RecursiveCharacterTextSplitter(
               chunk_size=1500,
               chunk_overlap=200,
               length_function=len
           )


           all_splits = text_splitter.split_documents(data)


           st.session_state.vectorstore = Chroma.from_documents(
               documents = all_splits,
               embedding = OllamaEmbeddings(model = "llama3.1")
           )


           st.session_state.vectorstore.persist()


   st.session_state.retriever = st.session_state.vectorstore.as_retriever()


   if 'qa_chain' not in st.session_state:
       st.session_state.qa_chain = RetrievalQA.from_chain_type(
           llm=st.session_state.llm,
           chain_type='stuff',
           retriever=st.session_state.retriever,
           verbose=True,
           chain_type_kwargs={
               "verbose": True,
               "prompt": st.session_state.prompt,
               "memory": st.session_state.memory,
           }
       )


   if user_input := st.chat_input("You:", key="user_input"):
       user_message = {"role": "user", "message": user_input}
       st.session_state.chat_history.append(user_message)
       with st.chat_message("user"):
           st.markdown(user_input)


       with st.chat_message("assistant"):
           with st.spinner("Assistant is typing..."):
               response = st.session_state.qa_chain(user_input)
           message_placeholder = st.empty()
           full_response = ""
           for chunk in response['result'].split():
               full_response += chunk + " "
               time.sleep(0.05)
               # Add a blinking cursor to simulate typing
               message_placeholder.markdown(full_response + "▌")
           message_placeholder.markdown(full_response)


       chatbot_message = {"role": "assistant", "message": response['result']}
       st.session_state.chat_history.append(chatbot_message)


else:
   st.write("Please upload a PDF file to start the chatbot")





