import requests
import json
import logging
from flask import jsonify

def add_agent(request):
    # Load the configuration file
    with open('config.json') as f:
        config = json.load(f)

    # Extract the API token and domain
    ZENDESK_API_TOKEN = config['ZENDESK_API_TOKEN']
    ZENDESK_DOMAIN = config['ZENDESK_DOMAIN']

    request_json = request.get_json(silent=True)
    if 'text' not in request_json:
        return jsonify(response_type='in_channel', text='Error: No email provided'), 400

    email = request_json['text']

    # Get the user ID associated with the email
    url = f"https://{ZENDESK_DOMAIN}.zendesk.com/api/v2/users/search.json?query={email}"
    headers = {"Authorization": f"Bearer {ZENDESK_API_TOKEN}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    user_data = response.json()
    if not user_data['users']:
        return jsonify(response_type='in_channel', text='Error: No user found with this email'), 400

    user_id = user_data['users'][0]['id']

    # Update the user role to agent
    url = f"https://{ZENDESK_DOMAIN}.zendesk.com/api/v2/users/{user_id}.json"
    data = {"user": {"role": "agent"}}

    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()

    return jsonify(response_type='in_channel', text=f'Successfully set user with email {email} to agent')
