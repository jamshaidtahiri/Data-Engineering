import os
import json
import google.auth
from flask import Flask, redirect, request, session, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

app = Flask(__name__)
app.secret_key = 'Random_Secret_Key'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Load the OAuth 2.0 client secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
API_SERVICE_NAME = "sheets"
API_VERSION = "v4"

# OAuth 2.0 flow object
flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri="http://localhost:5000/callback"
)

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    credentials = Credentials(**session['credentials'])
    service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Call the Sheets API
    spreadsheet_id = '1QeVhYdQHHycOs8IUO4EyUHrPA_38X2WV4A6NRPUzSqg'  # Replace with your Google Sheets ID
    range_name = 'Sheet1!A1:D10'  # Adjust the range as needed
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    return f"Data from Google Sheet: {values}"

@app.route('/authorize')
def authorize():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
