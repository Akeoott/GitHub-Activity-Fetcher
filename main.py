"""
README

This program, as explained in the Git repository, is designed to fetch user information
based on filtering (e.g., via a specific repo) or simply retrieving all publicly available 
data for a selected GitHub account.

The code is structured around user input. It is split into four functions:
1. user_input()
2. api_request()
3. response_parsing()
4. output_formatting()
"""

import requests, sys, pprint, json, time

# Credit coloring to CosmicBit128
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Variables to prevent repetetive links or text and make the code a tiny bit more readable
github_restapi_docs = "https://docs.github.com/rest/using-the-rest-api/troubleshooting-the-rest-api?apiVersion=2022-11-28"
github_token_docs = "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens"
github_token_docs_formated = f"Dont know how to get a {GREEN}token{RESET}?\n\033]8;;{github_token_docs}\033\\Visit this website.\033]8;;\033\\"

selection_error = f"\nSelect a {YELLOW}valid{RESET} option!"
token_print_format = f"{GREEN}token{RESET}"

def user_input():
    
    # Asking what to fetch
    fetch_type = None
    while fetch_type not in {1, 2}:
        try:
            print("Select what you want to fetch:")
            print(f"List {GREEN}user{RESET} events (1)")
            print(f"List {GREEN}repo{RESET} specific user events (2)")

            fetch_type = int(input("\nEnter here: "))

            if fetch_type not in {1, 2}:
                print(selection_error)
        except ValueError:
            print(selection_error)

    print()
    username = input(f"Enter the {GREEN}username{RESET} of the person you want to fetch from: ")
    UserAgent = input(f"Enter your {GREEN}app name{RESET} or {GREEN}identifier{RESET} (Can be anything): ")
    repo = None
    token = None

    # Selecting what url to use as one variable
    if fetch_type == 1:
        fetch_url_events = f'https://api.github.com/users/{username}/events'
    elif fetch_type == 2:
        repo = input(f"Enter the name of your {GREEN}repository{RESET}: ")
        fetch_url_events = f'https://api.github.com/repos/{username}/{repo}/events'

    # Asking for a token
    if fetch_type == 1:
        print(f"You {YELLOW}may{RESET} need a personal access {token_print_format}.")
        print(github_token_docs_formated)
        print("\nIf you dont want to enter a token, press enter!")
        token = input(f"Optional -> Enter your access {token_print_format}: ")

        if len(token) < 40:
            token = None

    elif fetch_type == 2:
        print(f"You {YELLOW}require{RESET} a personal access {token_print_format}.")
        print(github_token_docs_formated)
        token = input(f'\nEnter your access {token_print_format}: ')

    # Confirming input
    print("Is this correct?")
    print(f"Username: {GREEN}{username}{RESET}")
    print(f"App name or identifier: {GREEN}{UserAgent}{RESET}")
    print(f"Repository: {BLUE if repo == None else GREEN}{repo}{RESET}")
    print(f"Your token: {BLUE if token == None else GREEN}{token}{RESET}")

    confirm_user_input = input("Do you want to continue? (y/n): ").lower()
    if confirm_user_input == "y":
        pass
    else:
        print("Exiting...")
        time.sleep(3)
        sys.exit()

def api_request():
    pass

def response_parsing():
    pass

def output_formatting():
    pass

user_input()