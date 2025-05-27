# constants.py
VERSION = '4.0.0-beta'
INFO_TITLE = f"GitHub Activity Fetcher v{VERSION}"
WARNING_TITLE = f"WARNING - GitHub Activity Fetcher v{VERSION}"
ERROR_TITLE = f'ERROR - GitHub Activity Fetcher v{VERSION}'
ISSUE_INFO = "If the issue persists,\nPlease open an issue on GitHub\n'Akeoottt/GitHub-Activity-Fetcher/issues'"
ISSUE_INFO_HTML = "<b>If</b> the issue persists,<br>Please open an issue on GitHub<br>'Akeoottt/GitHub-Activity-Fetcher/issues'"

RESTAPI_DOCS = "https://docs.github.com/rest/using-the-rest-api/troubleshooting-the-rest-api?apiVersion=2022-11-28"

STATUS_MESSAGES = {
    404: "Not Found",
    403: "Forbidden",
    429: "Too Many Requests",
    400: "Bad Request",
    401: "Unauthorized (token invalid)",
    None: ""
}