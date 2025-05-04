import requests,sys,pprint,json,time
from colorama import Fore, init
init(autoreset=True)

GitHub_RESTAPI_docs = "https://docs.github.com/rest/using-the-rest-api/troubleshooting-the-rest-api?apiVersion=2022-11-28"
GitHub_token_docs = "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens"
GitHub_token_docs_formated = f"Dont know how to get a {Fore.GREEN}token{Fore.RESET}?\n\033]8;;{GitHub_token_docs}\033\\Visit this website.\033]8;;\033\\"

Select_Valid = f"\nSelect a {Fore.YELLOW}valid{Fore.RESET} option!"

try:
    # User input handling
    while True:
        try:
            print(f"Select what you want to fetch:\nList {Fore.GREEN}repository{Fore.RESET} events (enter 1)\nList {Fore.GREEN}user{Fore.RESET} events (enter 2)\n")
            
            # Asking what one specifically wants to fetch
            selected_fetch = int(input("Enter here: "))

            fetch_type_possible = {1,2}

            if selected_fetch in fetch_type_possible:
                break
            else:
                print(Select_Valid)
        except ValueError:
            print(Select_Valid)

    username = input(f"\nEnter the {Fore.GREEN}username{Fore.RESET} of the person you want to fetch from: ")
    UserAgent = input(f"Enter your {Fore.GREEN}app name{Fore.RESET} or {Fore.GREEN}identifier{Fore.RESET}: ")

    repo = None

    if selected_fetch == 1:
        repo = input(f"Enter the name of your {Fore.GREEN}repository{Fore.RESET}: ")

    url_events = f'https://api.github.com/users/{username}/events'
    url_repo_events = f'https://api.github.com/repos/{username}/{repo}/events'

    # Asking for a token
    token_print_format = f"{Fore.GREEN}token{Fore.RESET}"

    if selected_fetch == 1:
        print(f"You require a personal access {token_print_format}.")
        print(GitHub_token_docs_formated)
        token = input(f'\nEnter your access {token_print_format} (case sensitive): ')

    elif selected_fetch == 2:
        print(f"You {Fore.YELLOW}may{Fore.RESET} need a personal access {token_print_format} (higher rate limits).")
        print(GitHub_token_docs_formated)
        token = input(f'\nOptional -> Enter your access {token_print_format}. If not, enter "no" (case sensitive): ')
        if token == "no":
            token = None
    
    # Confirming input is correct
    print(f"\nIs this correct?\nUsername: {Fore.GREEN}{username}{Fore.RESET}\nApp name or identifier: {Fore.GREEN}{UserAgent}{Fore.RESET}\nRepository: {Fore.BLUE if repo == None else Fore.GREEN}{repo}{Fore.RESET}\nYour token: {Fore.BLUE if token == None else Fore.GREEN}{token}{Fore.RESET}\n")
    if token is None:
        print(f"(Your {token_print_format} is {Fore.BLUE}None{Fore.RESET}, reason is you either have entered it wrong or you didnt want to enter one)\n")

    confirm = input("Do you want to continue? (y/n): ").lower()
    if confirm == "y":
        pass
    else:
        print("Exiting...")
        time.sleep(3)
        sys.exit()

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
            print(f"\n{Fore.RED}Failed to parse JSON. GitHub may have returned HTML instead.")
            print("Raw response content:\n", response.text)
            input("\nPress Enter To Exit...")
            sys.exit()

        if not data:
            print(f"{Fore.YELLOW}No events found. The user or repository might be inactive or private.")

        print(f"\n{Fore.GREEN}User Events: ")
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
            if input(f"\n{Fore.GREEN}Save{Fore.RESET} as json? ({Fore.RED}will overwrite existing files with the same username!{Fore.RESET})\n(y/n): ").lower() == "y":
                with open(f"{username}-data.json", "w") as f:
                    json.dump(data, f, indent=4)
                print(f"\n{username}-data.json was {Fore.GREEN}created{Fore.RESET} in the same dir as this program!")
        
        except PermissionError as e:
            print(f"\nYou dont have the {Fore.RED}permission{Fore.RESET} to create a file in this directory.")
            print(f"{Fore.RED}{type(e).__name__}:{Fore.RESET} {e}")

    else:
        print(f"Error: {response.status_code}")
        print(f"More informations under: {GitHub_RESTAPI_docs}")

# Error handeling for unexpected errors as I often do silly mistakes
except Exception as e:
    print(f"\n{Fore.RED}An unexpected error occurred:")
    print(f"{Fore.RED}{type(e).__name__}:{Fore.RESET} {e}")
    print("\nPlease report this issue with the above error message on GitHub 'Akeoots/GitHub-Activity-Fetcher/issues'.")

# Exit sequence
input("\nPress Enter To Exit...")
sys.exit()