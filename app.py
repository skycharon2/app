import streamlit as st
import sqlite3

# Create SQLite database and table if not exist
conn = sqlite3.connect('user_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)''')
conn.commit()
conn.close()

# User registration
def register_user(username, email, password):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    conn.close()

# User login
def login(username, password):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Login form
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Sidebar for Login and Registration
if st.session_state['logged_in']:
    st.sidebar.write("Logged in!")
    
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
else:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if login(username, password):
            st.session_state['logged_in'] = True
        else:
            st.sidebar.write("Invalid credentials")
            
    if st.sidebar.button("Register"):
        email = st.sidebar.text_input("Email")
        register_user(username, email, password)

import streamlit as st
import PyPDF2
import openai

# Add balloons effect
st.balloons()

# Apply CSS styling to the chat window container
st.markdown("""
    <style>
        .chat-container {
            height: 300px;
            overflow-y: scroll;
        }
    </style>
""", unsafe_allow_html=True)

# PDF Extraction Function
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() for page in reader.pages])

# Sidebar
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    extracted_text = extract_text_from_pdf(uploaded_file)
    st.sidebar.text_area("Extracted text:", extracted_text)

# Spacer to move the username and email input down
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# Username and email at the bottom-left corner
username = st.sidebar.text_input("Enter your name:")
email = st.sidebar.text_input("Enter your email:")
st.sidebar.markdown(f"Welcome, {username}!")

# Main Content
st.image("/Users/nana/Desktop/logo.png", width=400)

# Spacer
st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)


import streamlit as st
import openai

openai.api_key = "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"

user_input = st.text_input('Ask me anything!', key='user_input')

if user_input:
    response = openai.Completion.create(engine="davinci", prompt=user_input, max_tokens=50)
    st.write(f"🐶: {response.choices[0].text}")


# Adding a Footer with Username and Email
st.markdown(f"""
    <footer style="position: fixed; left: 10px; bottom: 10px; color: white; background-color: rgba(0,0,0,0.1); padding: 10px; border-radius: 5px;">
        User: {username}
    </footer>
""", unsafe_allow_html=True)
