import base64
import logging
import os

import certifi
import requests

# Configure logging
logging.basicConfig(level = logging.INFO, format = "%(message)s")

# Load JIRA credentials from repo secrets
EMAIL = os.getenv("JIRA_EMAIL", "")
API_TOKEN = os.getenv("JIRA_API_TOKEN", "")

# Validate repository secrets
if not EMAIL or not API_TOKEN:
    raise EnvironmentError("Error: Repository secret not found.")

# JIRA API token config
basic_auth = f"{EMAIL}:{API_TOKEN}"
encoded_token = base64.b64encode(basic_auth.encode()).decode("utf-8")

# Reuse the HTTPS session to optimize requests
session = requests.Session()
session.verify = certifi.where()
session.headers.update(
    {
        "Authorization": f"Basic {encoded_token}",
        "Content-Type": "application/json"
    }
)