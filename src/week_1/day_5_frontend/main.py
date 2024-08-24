# # Create first streamlit app

# import streamlit as st
# import requests
# from Open_source import *

# chat_bot = chat_bot()



# # Initialize session state for tracking user input and responses
# if 'responses' not in st.session_state:
#     st.session_state.responses = []
    
# # Select model and training parameter
# selected_model =chat_bot.models[0]
# temperature =  1.5

# # Define the URL of the backend chat API
# backend_url = "http://127.0.0.1:5000/chat_batch"

# # Function to handle sending messages and receiving responses
# def handle_message(user_input):
#     if user_input:
#         # Add the user input to the session state
#         st.session_state.responses.append({'user': user_input, 'bot': None})
        
#         # Prepare an empty container to update the bot's response in real-time
#         response_container = st.empty()

#         # Send the user input to the backend API
#         response = requests.post(backend_url, json={"message": user_input, "model":selected_model, "temperature":temperature}, stream=True)

#         if response.status_code == 200:
            
#             st.text_area("Bot:", response.content, height=100)      
                
#         else:
#             response_container.markdown("<p style='color:red;'>Error: Unable to get a response from the server.</p>", unsafe_allow_html=True)

#         # Clear the input box for the next question
#         st.session_state.current_input = ""

# # Input text box for user input
# if 'current_input' not in st.session_state:
#     st.session_state.current_input = ""

# user_input = st.text_input("You:", st.session_state.current_input)

# if st.button("Send"):
#     handle_message(user_input)



import streamlit as st
import requests
from model import *

chat_bot = chat_bot()

# Initialize session state for tracking user input and responses
if 'responses' not in st.session_state:
    st.session_state.responses = []


# Function to handle sending messages and receiving responses
def handle_message(user_input, backend_url, selected_response_type, selected_model, set_tokens, temperature):
    if user_input:
        # Add the user input to the session state
        st.session_state.responses.append({'user': user_input, 'bot': None})
        
        # Prepare an empty container to update the bot's response in real-time
        response_container = st.empty()

        # Send the user input to the backend API
        response = requests.post(backend_url, json={"message": user_input, "model":selected_model, "temperature":temperature, "max_tokens":set_tokens}, stream=True)

        if response.status_code == 200:
            bot_response = ""

            if selected_response_type == chat_bot.output_type[0]:
                # Stream the response from the backend
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    bot_response += chunk
                    # Update the response container with the latest bot response
                    response_container.markdown(f"""
                    <div style="background-color:#f0f0f0; padding:10px; border-radius:5px;">
                        <p style="font-family:Arial, sans-serif;">{bot_response.strip()}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Update the latest bot response in session state
                st.session_state.responses[-1]['bot'] = bot_response.strip()
                
            else:
                # Collect the batch response
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    bot_response += chunk
                
                # Display the bot's response with adaptable height
                st.markdown(f"""
                <div style="background-color:#f0f0f0; padding:10px; border-radius:5px;">
                    <p style="font-family:Arial, sans-serif;">{bot_response.strip()}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Update the latest bot response in session state
                st.session_state.responses[-1]['bot'] = bot_response.strip()
                
        else:
            response_container.markdown("<p style='color:red;'>Error: Unable to get a response from the server.</p>", unsafe_allow_html=True)

        # Clear the input box for the next question
        st.session_state.current_input = ""


# Display the chat history
def display_chat_history():
    with st.container():
        for response in st.session_state.responses:
            st.markdown(f"""
            <div style="background-color:#e0e0e0; padding:10px; border-radius:5px;">
                <p style="font-family:Arial, sans-serif;"><strong>You:</strong> {response['user']}</p>
                <p style="font-family:Arial, sans-serif;"><strong>Bot:</strong> {response['bot']}</p>
            </div>
            """, unsafe_allow_html=True)


# Main layout
def main():
    
    # Display the chat history first
    display_chat_history()

    # Collect user inputs below the chat history
    with st.form(key='input_form', clear_on_submit=True):
        
        # Select model and training parameter
        selected_model = st.selectbox("Select your prefered model:", chat_bot.models)
        selected_response_type = st.selectbox("Select your preferred output type", chat_bot.output_type)
        temperature =  st.number_input("Enter the parameter for model temperature (Number must be a float between 0 and 2)", min_value=0.0, max_value=2.0, value=0.0, step=0.1, format="%.1f")
        set_tokens = st.selectbox("Please select how long you will want your output", chat_bot.token_class.keys())
        user_input = st.text_input("You:", "")

        # Submit button to send the input
        submit_button = st.form_submit_button(label="Send")

        # Define the URL of the backend chat API
        if selected_response_type == chat_bot.output_type[0]:
            backend_url = "http://127.0.0.1:5000/chat_stream"
        else:
            backend_url = "http://127.0.0.1:5000/chat_batch"

        if submit_button and user_input:
            handle_message(user_input=user_input, backend_url=backend_url, selected_response_type =selected_response_type, selected_model=selected_model, set_tokens=set_tokens, temperature=temperature)
            

if __name__ == "__main__":
    main()