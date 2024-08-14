"""Example script to access Claude models using GCP credentials"""

import json
from anthropic import AnthropicVertex
from google.oauth2 import service_account, credentials
# from google.auth.credentials import Credentials
# from credentials import oauth2callback


# Load your service account json from path
with open('./poised-list-432014-v1-8802854aebd7.json', 'r') as file:
    print("Loading credentials...")
    secrets = json.load(file)

_credentials = service_account.Credentials.from_service_account_info(
    secrets,
    scopes=['https://www.googleapis.com/auth/cloud-platform.read-only']
)

# Where the model is running. e.g. us-central1 or europe-west4 for haiku
regions = [
    "us-central1",
    "us-east5",
    "europe-west1",
    "europe-west4",
]

models = [
    "claude-3-5-sonnet@20240620",
    "claude-3-opus@20240229",
    "claude-3-haiku@20240307",
    "claude-3-sonnet@20240229"
]

print("Instantiating AnthropicVertex...")
client = AnthropicVertex(credentials=_credentials, project_id=secrets["project_id"], region=regions[1])

print("Starting Q&A system...\n")
message = client.messages.create(
    model=models[0],
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Hey Claude!",
        }
    ],
)
print(message.content[0].text)
