import requests
import certifi
from jira_auth import get_auth_header

def get_authenticated_session() -> requests.Session:
    session = requests.Session()
    session.verify = certifi.where()
    session.headers.update(get_auth_header())
    return session

'''
Imports requests to talk to API services over the internet.
Imports certifi to make sure we're communicating with secure websites.

When calling get_authenticated_session(), a Session object is returned.
It creates a new Session object that remembers headers/settings/etc.
Certifi provides a list of approved sites and forbids talking to sketchy ones.
Auth header is added to each request like a reusable ID badge.
'''