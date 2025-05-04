"""
README

This program, as explained in the Git repository, is designed to fetch user information
based on filtering (e.g., via a specific repo) or simply retrieving all publicly available 
data for a selected GitHub account.

The code is structured around user input. It is split into two phases:
1. Initial User Input
2. Post-Critical User Input
"""

import requests,sys,pprint,json,time

# Create color formatting escape codes
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'


# Variables to prevent repetetive links or text and make code a tiny bit more readable
GitHub_RESTAPI_docs = "https://docs.github.com/rest/using-the-rest-api/troubleshooting-the-rest-api?apiVersion=2022-11-28"
GitHub_token_docs = "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens"
GitHub_token_docs_formated = f"Dont know how to get a {GREEN}token{RESET}?\n\033]8;;{GitHub_token_docs}\033\\Visit this website.\033]8;;\033\\"

Select_Valid = f"\nSelect a {YELLOW}valid{RESET} option!"


# Initial User Input


try:
    # User input handling
    while True:
        try:
            # Asking what one specifically wants to fetch
            print(f"Select what you want to fetch:\nList {GREEN}repository{RESET} events (enter 1)\nList {GREEN}user{RESET} events (enter 2)\n")
            selected_fetch = int(input("Enter here: "))

            fetch_type_possible = {1,2}

            if selected_fetch in fetch_type_possible:
                break
            else:
                print(Select_Valid)
        except ValueError:
            print(Select_Valid)

    username = input(f"\nEnter the {GREEN}username{RESET} of the person you want to fetch from: ")
    UserAgent = input(f"Enter your {GREEN}app name{RESET} or {GREEN}identifier{RESET}: ")

    repo = None

    if selected_fetch == 1:
        repo = input(f"Enter the name of your {GREEN}repository{RESET}: ")

    url_events = f'https://api.github.com/users/{username}/events'
    url_repo_events = f'https://api.github.com/repos/{username}/{repo}/events'

    # Asking for a token
    token_print_format = f"{GREEN}token{RESET}"

    if selected_fetch == 1:
        print(f"You require a personal access {token_print_format}.")
        print(GitHub_token_docs_formated)
        token = input(f'\nEnter your access {token_print_format} (case sensitive): ')

    elif selected_fetch == 2:
        print(f"You {YELLOW}may{RESET} need a personal access {token_print_format} (higher rate limits).")
        print(GitHub_token_docs_formated)
        token = input(f'\nOptional -> Enter your access {token_print_format}. If not, enter "no" (case sensitive): ')
        if token == "no":
            token = None
    
    # Confirming input is correct
    print(f"\nIs this correct?\nUsername: {GREEN}{username}{RESET}\nApp name or identifier: {GREEN}{UserAgent}{RESET}\nRepository: {BLUE if repo == None else GREEN}{repo}{RESET}\nYour token: {BLUE if token == None else GREEN}{token}{RESET}\n")
    if token is None:
        print(f"(Your {token_print_format} is {BLUE}None{RESET}, reason is you either have entered it wrong or you didnt want to enter one)\n")

    confirm = input("Do you want to continue? (y/n): ").lower()
    if confirm == "y":
        pass
    else:
        print("Exiting...")
        time.sleep(3)
        sys.exit()


    # Post-Critical User Input


    headers = {
        'User-Agent': UserAgent,
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    if token:
        headers['Authorization'] = f'token {token}'

    # Selecting different ways to fetch specific data
    if selected_fetch == 1:
        response = requests.get(url_repo_events, headers=headers)
    elif selected_fetch == 2:
        response = requests.get(url_events, headers=headers)

    # Fetching and displaying User Events
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

        print(f"\n{GREEN}User Events: ")
        pprint.pprint(data)

        # Fetching rate limits
        rate_limit = response.headers.get('X-RateLimit-Limit')
        rate_remaining = response.headers.get('X-RateLimit-Remaining')
        rate_reset = response.headers.get('X-RateLimit-Reset')

        if token is None:
            print("\nSome information may not be present as you have not entered an access token!")

        print("\nRate Limit Information:")
        print(f"Rate Limit: {rate_limit} requests per hour")
        print(f"Remaining Requests: {rate_remaining} requests left")
        print(f"Rate Limit Reset at: {time.ctime(int(rate_reset))}")

        # Optionally creating json file
        try:
            if input(f"\n{GREEN}Save{RESET} as json? ({RED}will overwrite existing files with the same username!{RESET})\n(y/n): ").lower() == "y":
                with open(f"{username}-data.json", "w") as f:
                    json.dump(data, f, indent=4)

                print(f"\n{username}-data.json was {GREEN}created{RESET} in the same dir as this program!")
        
        except PermissionError as e:
            print(f"\nYou dont have the {RED}permission{RESET} to create a file in this directory.")
            print(f"{RED}{type(e).__name__}:{RESET} {e}")

    else:
        print(f"Error: {response.status_code}")
        print(f"More informations under: {GitHub_RESTAPI_docs}")

# Error handeling for unexpected errors as I often do silly mistakes
except Exception as e:
    print(f"\n{RED}An unexpected error occurred:")
    print(f"{RED}{type(e).__name__}:{RESET} {e}")
    print("\nPlease report this issue with the above error message on GitHub 'Akeoots/GitHub-Activity-Fetcher/issues'.")

# Exit sequence
input("\nPress Enter To Exit...")
sys.exit()
