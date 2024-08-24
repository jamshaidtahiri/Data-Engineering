import requests
url = 'https://github.com/jamshaidtahiri/Data-Engineering/issues'
access_token = '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'
headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {access_token}',
    'X-GitHub-Api-Version': '2022-11-28',
    'Content-Type': 'application/json',
}

data = '{"title":"Found a bug","body":"I am having a problem with this.","assignees":["jamshaidtahiri"],"labels":["bug"]}'

response = requests.post('https://api.github.com/repos/jamshaidtahiri/Data-Engineering/issues', 
                         headers=headers, 
                         data=data)

print(response.status_code)
print(response.content)