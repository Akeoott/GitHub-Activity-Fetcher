# Copyright (c) 2025 Akeoott <amejanin@gmail.com>. Licensed under the MIT Licence.
# See the LICENCE file in the repository root for full licence text.

"""
README

This program, as explained in the Git repository, is designed to fetch user information
based on filtering (e.g., via a specific repo) or simply retrieving all publicly available 
data for a selected GitHub account.

The code is structured around user input. It is split into five functions:
1. user_input()
2. api_request()
3. response_parsing()
4. data_saving()

WARNING!
This is fresh code which was created in one go and is very likely to have bugs.
If anything goes wrong, bring that to my attention asap.
"""

import requests, sys, os, pprint, json, time

VERSION = 'v2.0.0'

# Credit coloring to CosmicBit128
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Variables to prevent repetitive links or text and make the code a tiny bit more readable
RESTAPI_DOCS = "https://docs.github.com/rest/using-the-rest-api/troubleshooting-the-rest-api?apiVersion=2022-11-28"
TOKEN_DOCS = "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens"
TOKEN_DOCS_FORMATED = f"Dont know how to get a {GREEN}token{RESET}?\n\033]8;;{TOKEN_DOCS}\033\\Visit this website.\033]8;;\033\\"

SELECTION_ERROR = f"\nSelect a {YELLOW}valid{RESET} option!"
TOKEN_PRINT_FORMAT = f"{GREEN}token{RESET}"

print(VERSION)

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
                print(SELECTION_ERROR)
        except ValueError:
            print(SELECTION_ERROR)

    print()
    username = input(f"Enter the {GREEN}username{RESET} of the person you want to fetch from: ")
    useragent = input(f"Enter your {GREEN}app name{RESET} or {GREEN}identifier{RESET} (Can be anything): ")
    repo = None
    token = None

    # Selecting what url to use as one variable
    if fetch_type == 1:
        endpoint = f'https://api.github.com/users/{username}/events'
    elif fetch_type == 2:
        repo = input(f"Enter the name of your {GREEN}repository{RESET}: ")
        endpoint = f'https://api.github.com/repos/{username}/{repo}/events'

    # Asking for a token
    if fetch_type == 1:
        print(f"You {YELLOW}may{RESET} need a personal access {TOKEN_PRINT_FORMAT}.")
        print(TOKEN_DOCS_FORMATED)
        print("\nIf you dont want to enter a token, press enter!")
        token = input(f"Optional -> Enter your access {TOKEN_PRINT_FORMAT}: ")

        if token == "":
            token = None

    elif fetch_type == 2:
        print(f"You {RED}require{RESET} a personal access {TOKEN_PRINT_FORMAT}.")
        print(TOKEN_DOCS_FORMATED)
        token = input(f'\nEnter your access {TOKEN_PRINT_FORMAT}: ')

    # Confirming input
    print("\nIs this correct?")
    print(f"Username: {GREEN}{username}{RESET}")
    print(f"App name or identifier: {GREEN}{useragent}{RESET}")
    print(f"Repository: {BLUE if repo == None else GREEN}{repo}{RESET}")
    print(f"Your token: {BLUE if token is None else GREEN}{'[HIDDEN]' if token else 'None'}{RESET}")

    confirm_input = input("Do you want to continue? (y/n): ").lower()
    if confirm_input == "y":
        pass
    else:
        print("Exiting...")
        time.sleep(3)
        sys.exit()

    return endpoint, username, useragent, token


try:
    def api_request(endpoint, username, useragent, token):
        headers = {
            'User-Agent': useragent,
            'Accept': 'application/vnd.github.v3+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        if token:
            headers['Authorization'] = f'token {token}'

        response = requests.get(endpoint, headers=headers)

        # Fetching data
        if response.status_code == 200:
            try:
                data = response.json()
            except json.JSONDecodeError:
                print(f"\n{RED}Failed to parse JSON. GitHub may have returned HTML instead.")
                print("Raw response content:\n", response.text)
                input("\nPress Enter To Exit...")
                sys.exit()
            if not data:
                print(f"{YELLOW}No events found. The user or repository might be inactive or private.")
        else:
            status_messages = {
                404: "Not Found",
                403: "Forbidden",
                429: "Too Many Requests",
                400: "Bad Request",
                401: "Unauthorized (token invalid)"
            }
            status_error_message = status_messages.get(response.status_code, "")

            print(f"Code: {response.status_code} {status_error_message}")
            print(f"More information under: {RESTAPI_DOCS}")
            input("\nPress Enter To Exit...")
            sys.exit()

        # Fetching rate limits
        rate_limit = response.headers.get('X-RateLimit-Limit')
        rate_remaining = response.headers.get('X-RateLimit-Remaining')
        rate_reset = response.headers.get('X-RateLimit-Reset')

        return data, rate_limit, rate_remaining, rate_reset, token, username


    def output_formatting(data, rate_limit, rate_remaining, rate_reset, token, *args):

        print(f"\n{GREEN}User Events:{RESET} ")
        pprint.pprint(data)

        if token is None:
            print("\nSome information may not be present as you have not entered an access token!")

        print("\nRate Limit information:")
        print(f"Rate Limit: {rate_limit} requests per hour")
        print(f"Remaining Requests: {rate_remaining} requests left")
        print(f"Rate Limit Reset at: {time.ctime(int(rate_reset))}")


    def data_saving(data, username, *args):
        failed_to_save = False
        try:
            if input(f"\n{GREEN}Save{RESET} as json? ({RED}will overwrite existing files with the same username!{RESET})\n(y/n): ").strip().lower() == "y":
                with open(f"{username}-data.json", "w") as f:
                    json.dump(data, f, indent=4)

                print(f"\n{username}-data.json was {GREEN}created{RESET} in the same directory as this program!")
        
        except PermissionError as e:
            print(f"\nYou dont have the {RED}permission{RESET} to create a file in this directory.")
            print(f"{RED}{type(e).__name__}:{RESET} {e}\n")
            failed_to_save = True

        if failed_to_save:
            while True:
                directory = input(f"Enter an {YELLOW}alternative{RESET} directory path or {RED}exit{RESET} out of saving the file by pressing {GREEN}enter{RESET}: ")
                if directory == "":
                    break
                else:
                    if os.path.exists(directory):
                        if os.path.isdir(directory):
                            
                            filepath = os.path.join(directory, f"{username}-data.json")
                            with open(filepath, "w") as f:
                                json.dump(data, f, indent=4)

                            print(f"\n{username}-data.json was {GREEN}created{RESET} at: {filepath}")
                            break
                        else:
                            print("Path isnt a directory!")        
                    else:
                        print("Path does not exist!")


    # Calling functions and passing them on
    input_data = user_input()
    response = api_request(*input_data)
    output_formatting(*response)
    data_saving(response[0], response[5])

# Error handling for unexpected events
except Exception as e:
    print(f"\n{RED}An unexpected error occurred:")
    print(f"{RED}{type(e).__name__}:{RESET} {e}")
    print("\nPlease report this issue with the above error message on GitHub 'Akeoots/GitHub-Activity-Fetcher/issues'")

# informations
# Exit sequence
input("\nPress Enter To Exit...")
sys.exit()