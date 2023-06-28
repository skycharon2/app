import streamlit as st
import PyPDF2
import openai
from io import BytesIO
import requests

# Custom styling
st.markdown("""
    <style>
        .reportview-container .main {
            background-color: white;
        }
        div[data-testid="stSidebar"] .sidebar-content {
            background-color: orange;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### PDF Text Extractor")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    reader = PyPDF2.PdfFileReader(uploaded_file)
    text = " ".join([reader.getPage(i).extract_text() for i in range(reader.numPages)])
    st.sidebar.text_area("Extracted text:", text)

# Spacer to move the username and email input down
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# Username and email at the bottom-left corner
username = st.sidebar.text_input("Enter your name:")
email = st.sidebar.text_input("Enter your email:")
st.sidebar.markdown(f"Welcome, {username}!")
# Main Content
st.image("/Users/nana/Desktop/logo.png", width=400)  
# Spacer
st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", 
unsafe_allow_html=True)

# Create a text input for user query
user_input = st.text_input('Ask me anything!')

# Dummy response - here you can call the ChatGPT API for a real response
if user_input:
    api_key = 'your_api_key_here'
    response = openai.Completion.create(engine="davinci-codex", prompt=user_input, max_tokens=50)
    st.write(f"🐶: {response.choices[0].text}")

# Adding a Footer with Username and Email
st.markdown(f"""
    <footer style="position: fixed; left: 10px; bottom: 10px; color: white; background-color: 
rgba(0,0,0,0.1); padding: 10px; border-radius: 5px;">
        User: {username}
    </footer>
""", unsafe_allow_html=True)

