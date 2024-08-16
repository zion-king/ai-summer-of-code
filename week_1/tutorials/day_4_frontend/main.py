# Create first streamlit app

import streamlit as st
from model import ChatBot
import requests

chat_bot = ChatBot()

# Initialize session state for tracking user input and responses
if 'responses' not in st.session_state:
    st.session_state.responses = []
    
# Select model and training parameter
selected_model =chat_bot.models[0]
temperature =  1.5

# Define the URL of the backend chat API
backend_url = "http://127.0.0.1:5000/chat_batch"

# Function to handle sending messages and receiving responses
def handle_message(user_input):
    if user_input:
        # Add the user input to the session state
        st.session_state.responses.append({'user': user_input, 'bot': None})
        
        # Prepare an empty container to update the bot's response in real-time
        response_container = st.empty()

        # Send the user input to the backend API
        response = requests.post(backend_url, json={"message": user_input, "model":selected_model, "temperature":temperature}, stream=True)

        if response.status_code == 200:
            bot_response = ""
            
            # Collect the batch response
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                bot_response += chunk
            
            # Display the bot's response with adaptable height
            st.markdown(f"""
            <div style="background-color:#f0f0f0; padding:10px; border-radius:5px;">
                <p style="font-family:Arial, sans-serif;">{bot_response.strip()}</p>
            </div>
            """, unsafe_allow_html=True)
            
                
        else:
            response_container.markdown("<p style='color:red;'>Error: Unable to get a response from the server.</p>", unsafe_allow_html=True)

        # Clear the input box for the next question
        st.session_state.current_input = ""

# Input text box for user input
if 'current_input' not in st.session_state:
    st.session_state.current_input = ""
user_input = st.text_input("You:", st.session_state.current_input)

if st.button("Send"):
    handle_message(user_input)