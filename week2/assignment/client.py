import requests
from urllib.parse import urlencode

# Client credentials
client_id = '64SJECxX4GsHcEYMpJQQ1LjL8hi37P4cDoCtAPBs'
client_secret = 'jPtqKtvnLZdwp25HmtpBWPLQ94rq469IAhvCORkauvB1t3gcLK'
redirect_uri = 'http://localhost:8000/callback'

# Step 1: User Authorization
params = {
    'response_type': 'code',
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'scope': 'email',
}

authorize_url = f"http://localhost:5000/oauth/authorize?{urlencode(params)}"
print(f"Go to the following URL to authorize the client: {authorize_url}")

# Step 2: The user visits the URL and authorizes the app. You'll get an authorization code.

# Once you have the code:
authorization_code = input("Enter the authorization code: ")

# Step 3: Exchange the authorization code for an access token
token_url = "http://localhost:5000/oauth/token"
data = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret,
}

response = requests.post(token_url, data=data)
print("Access Token Response:")
print(response.json())

access_token = response.json().get('access_token')

# Step 4: Access the protected resource
headers = {
    'Authorization': f'Bearer {access_token}',
}

resource_url = "http://localhost:5000/api/resource"
resource_response = requests.get(resource_url, headers=headers)
print("Resource Response:")
print(resource_response.json())
