from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch
from flask_sqlalchemy import SQLAlchemy

# Tokenizer and Model for chatbot
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

predefined_responses = {
    "who are you?": "I am Beat Buddy, your music companion!",
    "who r u?": "I am Beat Buddy, your music companion!",
    "wh r u?": "I am Beat Buddy, your music companion!",
    "who r uh?": "I am Beat Buddy, your music companion!",
    "what are you?": "I am Beat Buddy, your music companion!",
    "what r u?": "I am Beat Buddy, your music companion!",
    "what r uh?": "I am Beat Buddy, your music companion!",
    "who created you?": "I was developed by the Beat Buddy Team.",
    "who invented you?": "I was developed by the Beat Buddy Team.",
    "developed by whom?": "I was developed by the Beat Buddy Team.",
    "who developed you?": "I was developed by the Beat Buddy Team."
}

def get_embedding(text):
    """Get the embedding for a given text input."""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        model_output = model(**inputs)
    return model_output.last_hidden_state.mean(dim=1)

# Hugging Face API Key
HUGGINGFACE_API_KEY = "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"

# Spotify API credentials
SPOTIFY_CLIENT_ID = "52ae5de4f6764fe1ad72b742a4aac33c"
SPOTIFY_CLIENT_SECRET = "9261732c29534bae8136616a0e39a041"

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/vyshn/please/Database/users.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Load intents from intents.json
with open('intents.json') as file:
    intents = json.load(file)

# Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Route for home page (login/signup included)
@app.route('/')
def home():
    return render_template('home.html')  # Home page with login and signup options

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('indexnew.html') 
    else:
        return redirect(url_for('home'))

# Login and Signup Routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Check if passwords match
        if password != confirm_password:
            return "Passwords do not match"
        
        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered"
        
        # Add new user to the database
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        # Log the user in after signup
        session['user_id'] = new_user.id
        return redirect(url_for('dashboard'))
    
    # Render signup page if it's a GET request
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    
    # Render login page if it's a GET request
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

# Chatbot and recommendation logic
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
COHERE_API_KEY = "b16VoC5GXt8nYeQTUsO7uy8ZjQg3h5bsuGGFn6hs"

def get_chat_response(user_input):
    user_input_lower = user_input.lower()

    # If the user explicitly asks for a song or music recommendation
    if "play" in user_input_lower or "tune" in user_input_lower or "song" in user_input_lower:
        return get_music_recommendations(user_input_lower)
    
    # Check for predefined responses first
    user_input_embedding = get_embedding(user_input_lower)
    for question, response in predefined_responses.items():
        question_embedding = get_embedding(question)
        similarity = cosine_similarity(user_input_embedding, question_embedding)

        if similarity >= 0.8:
            return response

    # If no predefined response matches, use Cohere API for generating a response
    co = cohere.Client(COHERE_API_KEY)
    try:
        response = co.generate(
            model='command-xlarge-nightly',
            prompt=user_input,
            max_tokens=50
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Error with Cohere API: {e}")
        return "Sorry, I'm having trouble responding right now."


def get_music_recommendations(query):
    try:
        results = sp.search(q=query, type='track', limit=5)
        tracks = results['tracks']['items']

        if not tracks:
            return []

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
