# Google Cloud Function for add_agent
def add_agent(request):
    import os
    import requests
    from flask import jsonify

    ZENDESK_API_TOKEN = os.environ['ZENDESK_API_TOKEN']
    ZENDESK_DOMAIN = os.environ['ZENDESK_DOMAIN']

    request_json = request.get_json(silent=True)
    user_id = request_json['text']

    url = f"https://{ZENDESK_DOMAIN}.zendesk.com/api/v2/users/{user_id}.json"
    headers = {"Authorization": f"Bearer {ZENDESK_API_TOKEN}"}
    data = {"user": {"role": "agent"}}
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()

    return jsonify(response_type='in_channel', text=f'Successfully set user {user_id} to agent')

# Google Cloud Function for remove_agent
def remove_agent(request):
    import os
    import requests
    from flask import jsonify

    ZENDESK_API_TOKEN = os.environ['ZENDESK_API_TOKEN']
    ZENDESK_DOMAIN = os.environ['ZENDESK_DOMAIN']

    request_json = request.get_json(silent=True)
    user_id = request_json['text']

    url = f"https://{ZENDESK_DOMAIN}.zendesk.com/api/v2/users/{user_id}.json"
    headers = {"Authorization": f"Bearer {ZENDESK_API_TOKEN}"}
    data = {"user": {"role": "end-user"}}
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()

    return jsonify(response_type='in_channel', text=f'Successfully removed agent permissions from user {user_id}')
