import logging, requests, os, json
from constants import STATUS_MESSAGES, RESTAPI_DOCS
import msg_handler # error handeler
from custom_exception import APIError
from tkinter import messagebox as msgbox

full_path = __file__
file_name = os.path.basename(full_path)

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
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": self.useragent
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def fetch_events(self):
        response = requests.get(self.endpoint, headers=self.headers)

        if response.status_code != 200:
            try:
                raise APIError(response.status_code, "Unexpected status code from API")
            except APIError as e:
                message = STATUS_MESSAGES.get(response.status_code, "")
                logging.debug(f"API Status code: {response.status_code} {message}")
                e_type: str = "error"
                context: str = (
                    f"A {type(e).__name__} unexpectedly occurred.<br>"
                    f"API Status code: {response.status_code} <b>{message}</b><br><br>"
                    f"More information under:<br>{RESTAPI_DOCS}"
                )
                msg_handler.error_handeling(e, e_type, context, file_name)

        logging.debug("API Status code: 200")

        data = None
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            e_type: str = "error"
            context: str = (
                f"A {type(e).__name__} unexpectedly occurred.<br>"
                f"Failed to Decode JSON."
            )
            msg_handler.error_handeling(e, e_type, context, file_name)
            data = {}  # or set to None, depending on how you want to handle this case

        logging.info("Successfully fetched data")

        # Extract rate limit headers from the same response
        headers = response.headers
        rate_limit_info = (
            headers.get("X-RateLimit-Limit", "?"),
            headers.get("X-RateLimit-Remaining", "?"),
            headers.get("X-RateLimit-Reset", "?")
        )

        return data, rate_limit_info