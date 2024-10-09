from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from waitress import serve

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get the API key from the environment variable
GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    books = []
    error = None
    theme = request.args.get('theme', 'quartz')  # Default theme is quartz

    if request.method == 'POST':
        try:
            # Get search parameters
            title = request.form.get('title', '')
            author = request.form.get('author', '')
            subject = request.form.get('subject', '')

            # Construct the query
            query = '+'.join(filter(None, [
                f'intitle:{title}' if title else '',
                f'inauthor:{author}' if author else '',
                f'subject:{subject}' if subject else ''
            ]))

            # Make a request to the Google Books API
            url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}'
            response = requests.get(url)
            data = response.json()

            # Check if there are any books returned
            if 'items' in data:
                books = data['items']
            else:
                error = "No books found matching your criteria."

        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template('index.html', books=books, error=error, theme=theme)

@app.route('/<theme>')
def themed_index(theme):
    return index()

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)