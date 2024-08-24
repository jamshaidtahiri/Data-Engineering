from flask import Flask, redirect, request, session, url_for
import requests
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify OAuth2 credentials
CLIENT_ID = "0b202af071a64896a74e81655f0bf0fe"
CLIENT_SECRET = "bff88fce4e294ab7b561028e1d456987"
REDIRECT_URI = "http://localhost:5000/callback"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"

# Define the scopes
SCOPE = "user-library-read"

@app.route('/')
def index():
    return '<h1>Welcome to the Spotify API</h1><a href="/login">Login with Spotify</a>'

@app.route('/login')
def login():
    auth_url = f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&scope={SCOPE}&redirect_uri={REDIRECT_URI}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    auth_response = requests.post(TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    session['token'] = auth_response_data['access_token']
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    token = session.get('token')

    if not token:
        return redirect(url_for('login'))

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{API_BASE_URL}/me", headers=headers)
    user_data = response.json()

    return f"<h1>Logged in as {user_data['display_name']}</h1><a href='/library'>View Saved Tracks</a>"

@app.route('/library')
def library():
    token = session.get('token')

    if not token:
        return redirect(url_for('login'))

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{API_BASE_URL}/me/tracks", headers=headers)
    tracks_data = response.json()

    return json.dumps(tracks_data, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
