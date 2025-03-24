# app.py - Main Flask application

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__)

# Set the API key provided
os.environ["GROQ_API_KEY"] = "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"  # You should rotate this key soon

# API endpoint for Groq
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-api-key')
def check_api_key():
    # Check if GROQ_API_KEY exists in environment variables
    api_key = os.environ.get('GROQ_API_KEY')
    return jsonify({'api_key_exists': bool(api_key)})

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        # Get the question from the request
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'})
        
        # Get API key
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key not configured'})
        
        # Prepare the request to Groq API
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'llama3-8b-8192',  # You can adjust the model as needed
            'messages': [
                {'role': 'system', 'content': 'You are a helpful medical assistant. Provide concise, accurate information about medical conditions and treatments.'},
                {'role': 'user', 'content': question}
            ],
            'temperature': 0.7,
            'max_tokens': 500
        }
        
        # Make the request to Groq API
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Process the response
        result = response.json()
        answer = result['choices'][0]['message']['content']
        
        # You can add more processing here if needed
        return jsonify({
            'answer': answer,
            'source': 'Groq LLM API By Sandipan Roy',
            'focus_area': 'Medical Information'
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request error: {str(e)}'})
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)