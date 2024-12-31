# app.py
from flask import Flask, request, render_template, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json

# Hugging Face API Key
HUGGINGFACE_API_KEY = "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"

# Spotify API credentials
SPOTIFY_CLIENT_ID = "52ae5de4f6764fe1ad72b742a4aac33c"
SPOTIFY_CLIENT_SECRET = "9261732c29534bae8136616a0e39a041"

# Flask app setup
app = Flask(__name__)

# Load intents from intents.json
with open('intents.json') as file:
    intents = json.load(file)

# Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

@app.route('/')
def home():
    return render_template('indexnew.html')  # Render the HTML page for the chat interface

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = get_chat_response(user_input)
    return jsonify({"response": response})

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.json.get('message')
    recommendations = get_music_recommendations(user_input)
    return jsonify({"response": recommendations})


import cohere

# Replace this with your Cohere API key
COHERE_API_KEY = "b16VoC5GXt8nYeQTUsO7uy8ZjQg3h5bsuGGFn6hs"

import cohere



def get_chat_response(user_input):
    co = cohere.Client(COHERE_API_KEY)
    try:
        response = co.generate(
            model='command-xlarge-nightly',  # Adjust model name as per availability
            prompt=user_input,
            max_tokens=50  # Adjust max tokens based on desired response length
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Error with Cohere API: {e}")
        return "Sorry, I'm having trouble responding right now."




def get_music_recommendations(query):
    try:
        # Search for tracks related to the user input
        results = sp.search(q=query, type='track', limit=5)
        tracks = results['tracks']['items']
        
        if not tracks:
            return []

        # Extract track names and Spotify URLs
        recommendations = [
            {"name": track['name'], "url": track['external_urls']['spotify']}
            for track in tracks
        ]
        return recommendations
    except Exception as e:
        print(f"Error fetching recommendations: {str(e)}")
        return []


if __name__ == "__main__":
    app.run(port=5000, debug=True)
