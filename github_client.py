from constants import MSGBOX_ERROR_OPEN_ISSUE_INFO, MSGBOX_ERROR_TITLE
import logging, requests, sys, json
from tkinter import messagebox as msgbox

RESTAPI_DOCS = "https://docs.github.com/rest/using-the-rest-api/troubleshooting-the-rest-api?apiVersion=2022-11-28"

STATUS_MESSAGES = {
    404: "Not Found",
    403: "Forbidden",
    429: "Too Many Requests",
    400: "Bad Request",
    401: "Unauthorized (token invalid)"
}

class GitHubAPIClient:
    def __init__(self, endpoint, username, useragent, token, repo):
        self.endpoint = endpoint
        self.username = username
        self.useragent = useragent
        self.token = token
        self.repo = repo
        self.headers = self._build_headers()
        logging.info(
            "github_client.py input:"
            f"endpoint: {self.endpoint}"
            f"username: {self.username}"
            f"useragent: {self.useragent}"
            f"token: {'[Hidden Token]' if self.token else '[No Token]'}"
            f"repo: {self.repo}"
            f"headers: {self.headers}"
        )

    def _build_headers(self):
        headers = {
            'User-Agent': self.useragent,
            'Accept': 'application/vnd.github.v3+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        if self.token:
            headers['Authorization'] = f'token {self.token}'
        return headers

    def fetch_events(self):
        response = requests.get(self.endpoint, headers=self.headers)

        if response.status_code != 200:
            self._handle_error(response)
        logging.debug("API Status code: 200")


        try:
            data = response.json()
        except json.JSONDecodeError as e:
            logging.error(f"Failed to Decode JSON: {e}")
            msgbox.showerror(title=MSGBOX_ERROR_TITLE, message=f"Failed to Decode JSON:\n{e}{MSGBOX_ERROR_OPEN_ISSUE_INFO}")
            sys.exit()

        logging.info("Successfully fetched data")
        return data, self._get_rate_limit_info()

    def _get_rate_limit_info(self):
        r = requests.get(self.endpoint, headers=self.headers).headers
        return (
            r.get("X-RateLimit-Limit", "?"),
            r.get("X-RateLimit-Remaining", "?"),
            r.get("X-RateLimit-Reset", "?")
        )

    def _handle_error(self, response):
        message = STATUS_MESSAGES.get(response.status_code, "")
        logging.error(f"API Status code: {response} {message}")
        msgbox.showerror(title=MSGBOX_ERROR_TITLE, message=f"API Status code: {response} {message}\nMore information under: {RESTAPI_DOCS}{MSGBOX_ERROR_OPEN_ISSUE_INFO}")
        sys.exit()