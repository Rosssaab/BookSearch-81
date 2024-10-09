import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get the API key from the environment variable
GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')

@app.route('/', methods=['GET', 'POST'])
@app.route('/<theme>', methods=['GET', 'POST'])
def index(theme='quartz'):
    books = []
    error = None
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        subject = request.form.get('subject')
        
        # Construct the search query
        query = f"{title} {author} {subject}".strip()
        
        # Make a request to the Google Books API
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            books = response.json().get('items', [])
        else:
            error = "An error occurred while searching for books."
    
    # List of valid Bootswatch themes
    valid_themes = ['cerulean', 'cosmo', 'cyborg', 'darkly', 'flatly', 'journal', 'litera', 'lumen', 'lux', 'materia', 'minty', 'pulse', 'sandstone', 'simplex', 'sketchy', 'slate', 'solar', 'spacelab', 'superhero', 'united', 'yeti', 'quartz']
    
    # If the provided theme is not valid, default to 'quartz'
    if theme.lower() not in valid_themes:
        theme = 'quartz'
    
    return render_template('index.html', books=books, error=error, theme=theme)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)