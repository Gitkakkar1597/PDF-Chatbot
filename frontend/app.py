import streamlit as st
import requests

# FastAPI endpoints
UPLOAD_URL = "http://127.0.0.1:8000/upload_pdf/"
QUERY_URL = "http://127.0.0.1:8000/query/"

# Title and description
st.title("PDF Chatbot")
st.write("Upload a PDF and ask questions about its contents.")

# PDF file upload
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    # Convert file to bytes
    file_bytes = uploaded_file.read()
    files = {"file": (uploaded_file.name, file_bytes, uploaded_file.type)}
    response = requests.post(UPLOAD_URL, files=files)
    
    if response.status_code == 200:
        st.success("PDF uploaded and processed successfully.")
    else:
        st.error(response.json().get("detail"))

# Initialize chat history and input state if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "query_input" not in st.session_state:
    st.session_state.query_input = ""

def submit_query():
    query = st.session_state.query_input
    if query:
        with st.spinner("Generating response..."):
            response = requests.post(QUERY_URL, json={"query": query})
            if response.status_code == 200:
                bot_response = response.json().get("response")
                # Update chat history
                st.session_state.chat_history.append({"query": query, "response": bot_response})
                # Clear the input field
                st.session_state.query_input = ""
            else:
                st.error(response.json().get("detail"))
    else:
        st.warning("Please enter a query.")

# Main layout
with st.container():
    st.subheader("Chat History:")
    
    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            # Display query and response
            st.write(f"**You:** {chat['query']}")
            st.write(f"**Bot:** {chat['response']}")
            # Display separator line
            st.markdown("---")
    else:
        st.write("No chat history yet.")

    # Check if a PDF is uploaded before showing the query section
    if uploaded_file:
        st.subheader("Ask questions about the PDF")

        # Input for new query
        query_input = st.text_input("Enter your query", key="query_input", on_change=submit_query)

