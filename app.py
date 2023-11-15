from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Render the search page without any results
    return render_template('index.html', results=None)

@app.route('/search', methods=['POST'])
def search():
    # Take the query and redirect to the result route
    query = request.form['query']
    return redirect(url_for('result', query=query))

@app.route('/result')
def result():
    # Get the query from the URL parameter
    query = request.args.get('query', '')
    if query:
        results = search_google(query)
        # Render the template with the results
        return render_template('index.html', results=results)
    # If no query was provided, redirect to the homepage
    return redirect(url_for('index'))

def search_google(query):
    # URL encode the query for the search
    query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={query}"

    # Set headers to simulate a request from a web browser
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

    # Perform the request and parse with BeautifulSoup
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Google's search results are in the 'div' with class 'BNeawe s3v9rd AP7Wnd'.
    # NOTE: This class name can change over time.
    paragraphs = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
    if paragraphs:
        # Return the text of the first relevant paragraph
        return paragraphs[0].get_text()

    # If no paragraphs are found, return a default message
    return "No results found."

if __name__ == '__main__':
    app.run(debug=True)
