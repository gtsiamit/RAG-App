import streamlit as st
from rag_backend import RAG
from utils import load_variables, get_current_datetime


def run_ui_app(llm_rag: RAG):
    """
    Run the Streamlit UI for the AI RAG Assistant.
    Args:
        llm_rag (RAG): An instance of the RAG class that handles the backend logic.
    """

    # Set the page configuration for the Streamlit app
    st.set_page_config(page_title="RAG AI Assistant", layout="centered")

    # Set the title of the Streamlit app
    st.title("RAG AI Assistant")

    # Initialize the session state for messages if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the chat messages from the session state
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input field for user to ask questions
    prompt = st.chat_input("Ask me anything...")
    # If the user has provided a prompt, the process continues
    if prompt:
        # Append the user input to the session state messages
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display the user input
        with st.chat_message("user"):
            st.markdown(prompt)

        # Loading spinner while the input is passed to the model
        with st.spinner("Processing..."):
            # Invoke the rag backend to get a response
            response = llm_rag.invoke(input_question=prompt)

        # Append the model's response to the session state messages
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display the model's response
        with st.chat_message("assistant"):
            st.markdown(response)


def main():
    """
    Main function to run the Streamlit app for the RAG AI Assistant.
    """

    # Load configuration variables from the JSON file
    # Get the chat model and embeddings model names and
    # the path to the documents from the loaded variables
    chat_model, embeddings_model, docs_path = load_variables()

    # Check if the chatbot instance already exists in the session state
    if "chatbot" not in st.session_state:
        # If not, create a new RAG instance with a unique thread id
        thread_id = f"thread-{get_current_datetime()}"
        st.session_state.chatbot = RAG(
            chat_model=chat_model,
            embeddings_model=embeddings_model,
            docs_path=docs_path,
            thread_id=thread_id,
        )

    # Run the Streamlit UI app with the llm rag instance
    run_ui_app(st.session_state.chatbot)


if __name__ == "__main__":
    main()
