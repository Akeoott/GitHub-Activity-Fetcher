import logging, requests, sys, json

RESTAPI_DOCS = "https://docs.github.com/rest/using-the-rest-api/troubleshooting-the-rest-api?apiVersion=2022-11-28"
RESET, GREEN, YELLOW, RED = '\033[0m', '\033[92m', '\033[93m', '\033[91m'

class GitHubAPIClient:
    pass