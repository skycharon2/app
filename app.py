import streamlit as st
import sqlite3
import PyPDF2
import openai

# Database
conn = sqlite3.connect('user_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS pdf_files (id INTEGER PRIMARY KEY, filename TEXT, extracted_text TEXT)''')
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

# Function to extract summary from PDF
def extract_summary_from_pdf(pdf_text):
    paragraphs = pdf_text.split('\n\n')
    summary = paragraphs[0]
    return summary

# Function to search PDF text based on user prompt
def search_pdf_text(prompt, pdf_text):
    return prompt in pdf_text

# Function to upload PDF and extract text
def upload_pdf_file(file):
    extracted_text = extract_text_from_pdf(file)
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO pdf_files (filename, extracted_text) VALUES (?, ?)", (file.name, extracted_text))
    conn.commit()
    conn.close()

# Login form
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Sidebar for Login and Registration
if st.session_state['logged_in']:
    username = st.session_state['username']
    st.sidebar.write(f"Logged in as {username}!")

    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
else:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if login(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
        else:
            st.sidebar.write("Invalid credentials")

    if st.sidebar.button("Register"):
        email = st.sidebar.text_input("Email")
        register_user(username, email, password)

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

# OpenAI
openai.api_key = "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"

# Sidebar for PDF upload
if st.session_state['logged_in']:
    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file:
        upload_pdf_file(uploaded_file)
        st.sidebar.text("PDF uploaded successfully.")

# Main Content
image_url = "https://i.imgur.com/bBejMa7.png"
st.image(image_url, width=400)

# Spacer
st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# OpenAI
user_input = st.text_input('Ask me anything!', key='user_input')

if user_input:
    if st.session_state['logged_in']:
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("SELECT extracted_text FROM pdf_files")
        rows = c.fetchall()
        pdf_texts = [row[0] for row in rows]
        conn.close()

        for pdf_text in pdf_texts:
            if search_pdf_text(user_input, pdf_text):
                st.write("📚 The answer can be found in the PDF.")
                break
        else:
            try:
                response = openai.Completion.create(engine="davinci", prompt=user_input, max_tokens=50)
                if response.choices and response.choices[0].text:
                    st.write(f"🐶: {response.choices[0].text}")
                else:
                    st.write("No response from the model.")
            except Exception as e:
                st.write(f"Error: {str(e)}")
    else:
        try:
            response = openai.Completion.create(engine="davinci", prompt=user_input, max_tokens=50)
            if response.choices and response.choices[0].text:
                st.write(f"🐶: {response.choices[0].text}")
            else:
                st.write("No response from the model.")
        except Exception as e:
            st.write(f"Error: {str(e)}")

# Adding a Footer with Username and Email
st.markdown(f"""
    <footer style="position: fixed; left: 10px; bottom: 10px; color: white; background-color: rgba(0,0,0,0.1); padding: 10px; border-radius: 5px;">
        User: {username if st.session_state['logged_in'] else 'Guest'}
    </footer>
""", unsafe_allow_html=True)
