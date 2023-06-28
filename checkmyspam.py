
import requests
import json

# Replace with your Office 365 credentials
client_id = '6bcb3b28-f008-4efe-95f6-4ca7c704a35e'
client_secret = 'sDn8Q~TB~_L8q7-74P4f~wsI0nP3K~SA7ZHl6aiQ'
tenant_id = 'f8cdef31-a31e-4b4a-93e4-5f571e91255a'

# Microsoft Graph API endpoint for accessing user mailbox messages
graph_api_endpoint = 'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages'

# Get access token
def get_access_token():
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': 'https://graph.microsoft.com/.default'
    }

    response = requests.post(token_url, headers=headers, data=data)
    response_data = response.json()
    access_token = response_data['access_token']
    return access_token

# Make a GET request to the Graph API endpoint
def make_api_call(access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Accept': 'application/json'
    }

    response = requests.get(graph_api_endpoint, headers=headers)
    response_data = response.json()
    return response_data

# Main script execution
if __name__ == '__main__':
    access_token = get_access_token()
    response_data = make_api_call(access_token)

    # Process the response
    if 'error' in response_data:
        print('An error occurred:')
        print(response_data['error']['message'])
    else:
        print('Received mails:')
        print('---------------------')
        for message in response_data['value']:
            print('Subject:', message['subject'])
            print('Received:', message['receivedDateTime'])
            print('Sender:', message['sender']['emailAddress']['name'])
            print('---------------------')
