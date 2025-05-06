import time, sys

RESET, GREEN, BLUE, YELLOW, RED = '\033[0m', '\033[92m', '\033[94m', '\033[93m', '\033[91m'
TOKEN_DOCS = "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens"
TOKEN_DOCS_FORMATTED = f"Dont know how to get a {GREEN}token{RESET}?\n\033]8;;{TOKEN_DOCS}\033\\Visit this website.\033]8;;\033\\"
TOKEN_PRINT_FORMAT = f"{GREEN}token{RESET}"
SELECTION_ERROR = f"\nSelect a {YELLOW}valid{RESET} option!"

class UserInputHandler:
    pass