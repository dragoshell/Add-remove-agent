from flask import Flask, request
import requests
import json

app = Flask(__name__)

@app.route('/zendesk', methods=['POST'])
def zendesk():
    command = request.form['text'].split(' ')[0]
    email = request.form['text'].split(' ')[1]

    if command == 'add':
        add_agent_permission(email)
    elif command == 'remove':
        remove_agent_permission(email)

    return 'Command processed', 200

def add_agent_permission(email):
    url = f'https://your_zendesk_subdomain.zendesk.com/api/v2/users/{email}'
    headers = {'Authorization': 'Bearer ' + 'your_zendesk_api_token'}
    data = {'user': {'role': 'agent'}}
    response = requests.put(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print('User role updated to agent')
    else:
        print('Error updating user role:', response.content)

def remove_agent_permission(email):
    url = f'https://your_zendesk_subdomain.zendesk.com/api/v2/users/{email}'
    headers = {'Authorization': 'Bearer ' + 'your_zendesk_api_token'}
    data = {'user': {'role': 'end-user'}}
    response = requests.put(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print('User role updated to end-user')
    else:
        print('Error updating user role:', response.content)

if __name__ == '__main__':
    app.run(port=3000)
