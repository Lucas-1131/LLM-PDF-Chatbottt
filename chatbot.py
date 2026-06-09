# An example LLM chatbot using Cohere API and Streamlit that references multiple PDFs
# Adapted from the StreamLit OpenAI Chatbot example - https://github.com/streamlit/llm-examples/blob/main/Chatbot.py

import streamlit as st
import cohere
import fitz # An alias for the PyMuPDF library.
import os

# Set page config for a cleaner, centered layout
st.set_page_config(page_title="Habitat HK Assistant", layout="centered")

# Initialize app state tracking for the start screen
if "started" not in st.session_state:
    st.session_state["started"] = False

def pdf_to_documents(pdf_path):
    """
    Converts a PDF to a list of 'documents' which are chunks of a larger document that can be easily searched 
    and processed by the Cohere LLM.
    """
    if not os.path.exists(pdf_path):
        return []

    try:
        doc = fitz.open(pdf_path)
        documents = []
        text = ""
        chunk_size = 1000
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            part_num = 1
            for i in range(0, len(text), chunk_size):
                documents.append({"title": f"{os.path.basename(pdf_path)} - Page {page_num + 1} Part {part_num}", "snippet": text[i:i + chunk_size]})
                part_num += 1
        return documents
    except Exception as e:
        return []

# Check if a valid Cohere API key is found in the secrets file
api_key_found = False
if hasattr(st, "secrets"):
    if "COHERE_API_KEY" in st.secrets.keys():
        if st.secrets["COHERE_API_KEY"] not in ["", "PASTE YOUR API KEY HERE"]:
            api_key_found = True

# Add a sidebar to the Streamlit app
with st.sidebar:
    st.header("Settings")
    if api_key_found:
        cohere_api_key = st.secrets["COHERE_API_KEY"]
        st.success("🔑 API Key Loaded")
    else:
        cohere_api_key = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
        st.markdown("[Get a Cohere API Key](https://dashboard.cohere.ai/api-keys)")
    
    st.write("---")
    st.header("Knowledge Base Status")
    
    # Automatically read and combine ALL resources without drop-down tabs
    my_documents = []
    my_documents.extend(pdf_to_documents('docs/habitat_mission_vision.pdf'))
    my_documents.extend(pdf_to_documents('docs/habitat_volunteer_faq.pdf'))
    
    if len(my_documents) > 0:
        st.info("📚 Active Knowledge Base: Loaded references from your files.")
    else:
        st.warning("⚠️ Ready for files! Place `habitat_mission_vision.pdf` and `habitat_volunteer_faq.pdf` inside your `docs/` folder.")

# --- UI LOGIC INTERFACE ---

# SCREEN 1: Starting Welcome Page
if not st.session_state["started"]:
    st.write("") 
    st.write("")
    st.title("🏡 Habitat for Humanity Hong Kong")
    st.subheader("Hello, welcome!")
    st.write("This is the Habitat for Humanity chatbot. What can I help you with today?")
    st.write("Click the button below to initialize the system and begin consulting our documentation.")
    
    # Clicking this switches session state to True and refreshes the script onto the chat screen
    if st.button("Start Chatbot", type="primary"):
        st.session_state["started"] = True
        st.rerun()

# SCREEN 2: The Chat Interface
else:
    # Set the title of the Streamlit app
    st.title("💬 Habitat for Humanity Hong Kong Assistant")
    
    # Provide an option to go back to the start page if desired
    if st.button("← Back to Welcome Page"):
        st.session_state["started"] = False
        st.rerun()
        
    st.write("---")

    # Initialize the chat history using Cohere-approved strictly verified roles
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{
            "role": "Chatbot", 
            "text": "Welcome! I'm the Habitat for Humanity Hong Kong Assistant. Ask me anything about our mission, our local programs like Project Home Works, or how you can get involved!"
        }]

    # Display the chat messages with customized icons natively
    for msg in st.session_state.messages:
        # Map User and Chatbot keys to custom emojis
        avatar_icon = "🏢" if msg["role"] == "Chatbot" else "👤"
        st.chat_message(msg["role"], avatar=avatar_icon).write(msg["text"])

    # Get user input
    if prompt := st.chat_input():
        # Stop responding if the user has not added the Cohere API key
        if not cohere_api_key:
            st.info("Please add your Cohere API key to continue.")
            st.stop()

        # Create a connection to the Cohere API
        client = cohere.Client(api_key=cohere_api_key)
        
        # Display the user message in the chat window with user icon
        st.chat_message("User", avatar="👤").write(prompt)

        # Clean, action-focused preamble for Habitat for Humanity Hong Kong
        preamble = "You are a helpful, warm, and informative chatbot representative for Habitat for Humanity Hong Kong. Your goal is to answer questions directly using the provided documents. Always adopt a passionate, community-driven, and respectful tone. If asked about the mission, state that it is to bring people together to improve living conditions for low-income families and vulnerable groups, helping them build strength, stability, and self-reliance. Focus on their core local programs: 'Project Home Works' and 'Project School Works'. If asked about volunteering or donating, explain the practical steps on how people can join these projects based on the documents. If the answer cannot be found in the document, answer to the best of your knowledge and politely direct them to check habitat.org.hk."

        # Send the user message and pdf text to the model and capture the response
        response = client.chat(chat_history=st.session_state.messages,
                               message=prompt,
                               documents=my_documents if len(my_documents) > 0 else None,
                               prompt_truncation='AUTO',
                               preamble=preamble)
        
        # Add the messages to the history using valid Cohere role names
        st.session_state.messages.append({"role": "User", "text": prompt})
        st.session_state.messages.append({"role": "Chatbot", "text": response.text})

        # Write the response to the chat window with organization icon
        st.chat_message("Chatbot", avatar="🏢").write(response.text)
        
        # Force instantaneous rerun to completely bypass the execution delay bug
        st.rerun()