from flask import Flask, redirect, request, session
import requests

app = Flask(__name__)
app.secret_key = 'your_static_secret_key'  # Replace with a secure, static key

# Replace these with your values
client_id = 'Ov23liEYsZ7FgXocSGFB'
client_secret = 'e8dea4c294fc6d3643cbb699faf22c6a92dfb210'
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
redirect_uri = 'http://localhost:5000/callback'

@app.route('/')
def index():
    return '<a href="/login">Login with GitHub</a>'

@app.route('/login')
def login():
    scopes = 'repo'
    # Redirect the user to GitHub's authorization page
    authorization_url = (f"{authorization_base_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}")
    # authorization_url = f"{authorization_base_url}?client_id={client_id}&redirect_uri={redirect_uri}"
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    # GitHub redirects back with a code; exchange it for an access token
    code = request.args.get('code')
    token_request_payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }
    token_response = requests.post(token_url, data=token_request_payload, headers={'Accept': 'application/json'})
    token_json = token_response.json()
    session['oauth_token'] = token_json.get('access_token')
    return redirect('/profile')

@app.route('/profile')
def profile():
    # Use the token to access GitHub's API and fetch user information
    if 'oauth_token' not in session:
        return redirect('/login')
    
    headers = {'Authorization': f"token {session.get('oauth_token')}"}
    user_info_response = requests.get('https://api.github.com/user', headers=headers)
    
    if user_info_response.status_code == 200:
        user_info = user_info_response.json()
        return f'Hello, {user_info["login"]}!<br>Your GitHub ID is {user_info["id"]}.'
    else:
        return 'Failed to retrieve profile information', 400

@app.route('/repos')
def repos():
    # Use the token to access GitHub's API and fetch user repositories
    if 'oauth_token' not in session:
        return redirect('/login')
    
    headers = {'Authorization': f"token {session.get('oauth_token')}"}
    repos_response = requests.get('https://api.github.com/user/repos', headers=headers)
    
    if repos_response.status_code == 200:
        repos = repos_response.json()
        repos_list = '<ul>'
        for repo in repos:
            repos_list += f'<li>{repo["name"]}</li>'
        repos_list += '</ul>'
        return f'Your repositories:<br>{repos_list}'
    else:
        return 'Failed to retrieve repositories', 400

@app.route('/create_repo')
def create_repo():
    headers = {
        'Authorization': f"token {session.get('oauth_token')}",
        'Accept': 'application/vnd.github+json'
    }
    data = {
        "name": "new-repo-from-flask",  # Name of the repository
        "description": "This is a new repository created via Flask app",
        "private": False,  # Set to True if you want a private repo
        "homepage":"https://github.com",
        "is_template":True
    }
    create_repo_response = requests.post('https://api.github.com/user/repos', json=data, headers=headers)
    if create_repo_response.status_code == 201:
        return 'Repository created successfully!'
    else:
        return f'Failed to create repository. Status Code: {create_repo_response.status_code}', 400

if __name__ == '__main__':
    app.run(debug=True)
