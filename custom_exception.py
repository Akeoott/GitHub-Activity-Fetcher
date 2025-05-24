from constants import STATUS_MESSAGES

class APIError(Exception):
    def __init__(self, status_code, message="API request failed"):
        self.STATUS_MESSAGES = STATUS_MESSAGES
        self.status_code = status_code
        self.message = message

        self.status_msg = self.STATUS_MESSAGES.get(self.status_code, "")
        super().__init__(f"{self.message} with status code {self.status_code} {self.status_msg}")