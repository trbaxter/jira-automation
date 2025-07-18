import requests
import certifi
from jira_auth import get_auth_header

def get_authenticated_session() -> requests.Session:
    session = requests.Session()
    session.verify = certifi.where()
    session.headers.update(get_auth_header())
    return session