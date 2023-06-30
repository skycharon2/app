import sqlite3
import PyPDF2
from langchain import LangChain

# Connect to the database
conn = sqlite3.connect('embeddings.db')

# Create a table if it doesn't exist
conn.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        embeddings BLOB
    )
''')

# Specify the path to the PDF file
pdf_file = '/Users/nana/app/file.pdf'

# Extract text from the PDF file
with open(pdf_file, 'rb') as file:
    reader = PyPDF2.PdfFileReader(file)
    content = ' '.join([reader.getPage(i).extract_text() for i in range(reader.numPages)])

# Insert the document and embeddings into the database
conn.execute('INSERT INTO documents (title, content, embeddings) VALUES (?, ?, ?)', ('file.pdf', content, embeddings))
conn.commit()

# Close the database connection
conn.close()
