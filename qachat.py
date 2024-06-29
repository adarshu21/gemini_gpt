from dotenv import load_dotenv
load_dotenv()  ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai


def configure_genai():
  """Configures the genai library with the API key from environment variables"""
  try:
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
  except (KeyError, ValueError) as e:
    st.error(f"Error configuring gena   i: {e}")
    st.stop()  # Halt execution if configuration fails


def get_gemini_response(question, chat):
  """Sends the message to the chat session and handles potential errors"""
  try:
    response = chat.send_message(question, stream=True)
    return response
  except (ValueError, ConnectionError) as e:
    st.error(f"Error getting response from Gemini: {e}")
    return None


def main():
  """Main function to run the Streamlit app"""
  configure_genai()

  model = genai.GenerativeModel("gemini-pro")
  chat = model.start_chat(history=[])

  st.set_page_config(page_title="Q&A Demo")
  st.header("Gemini MENTAL HEALTH BOT")

  # Initialize session state for chat history if it doesn't exist
  if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

  input_text = st.text_input("Input: ", key="input")
  submit_button = st.button("Ask the question")

  if submit_button and input_text:
    response = get_gemini_response(input_text, chat)
    if response:
      # Add user query and response to session state chat history
      st.session_state['chat_history'].append(("You", input_text))
      st.subheader("The Response is")
      for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
    else:
      # Handle cases where response retrieval fails
      st.warning("Failed to receive a response from Gemini.")

  st.subheader("The Chat History is")
  for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")


if __name__ == "__main__":
  main()
