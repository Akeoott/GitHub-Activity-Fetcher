import requests,sys,pprint,json
from colorama import Fore, Style, init
init(autoreset=True)

GitHub_token_docs = "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens"
GitHub_RESTAPI_docs = "https://docs.github.com/rest/using-the-rest-api/troubleshooting-the-rest-api?apiVersion=2022-11-28"

try:
    while True:

        # User input handling
        while True:
            try:
                print("Select what you want to fetch:\nList repository events (enter 1)\nList events for the authenticated user (enter 2)\n")
                
                # Asking what one specifically wants to fetch
                selected_fetch = int(input("Enter here: "))

                possible_selection = {1,2}

                if selected_fetch in possible_selection:
                    break
                else:
                    print("\nSelect a valid option!")
            except ValueError:
                print("\nSelect a valid option!!!")

        username = input("\nWhats the username of the person you want to fetch from: ")
        UserAgent = input('Enter your app name or identifier: ')

        repo = None

        if selected_fetch == 1:
            repo = input("Enter the name of your repository: ")

        url_events = f'https://api.github.com/users/{username}/events'
        url_repo_events = f'https://api.github.com/repos/{username}/{repo}/events'

        # Asking for a token
        while True:
            if selected_fetch == 1:
                print("You require a personal access token.")
                print("Dont know how to get a token? ", end='')
                print(f"\033]8;;{GitHub_token_docs}\033\\Visit this website.\033]8;;\033\\")

                token = input('\nEnter your access token (case sensitive): ')
                break

            elif selected_fetch == 2:
                print("You may want to use a personal access token.")
                print("Dont know how to get a token? ", end='')
                print(f"\033]8;;{GitHub_token_docs}\033\\Visit this website.\033]8;;\033\\")

                token = input('\nOptional -> Enter your access token. If not, enter "no" (case sensitive): ')
                if token == "no":
                    token = None
                break
        break
    
    # Confirming input is correct
    print(f"\nIs this correct?\nUsername: {username}\nApp name or identifier: {UserAgent}\nRepository: {repo}\nYour token: {token}\n")
    if token is None:
        print("(Your token is None, reason is you either have entered it wrong or you didnt want to enter one)\n")

    while True:
        confirm = input("Do you want to continue? (y/n): ").lower()
        print()
        if confirm == "y":
            break
        else:
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

    # Fetchng and displaying User Events
    if response.status_code == 200:
        data = response.json()

        print(f"\n{Fore.GREEN}User Events: ")
        pprint.pprint(data)

        str_data = data

        # Fetching rate limits
        rate_limit = response.headers.get('X-RateLimit-Limit')
        rate_remaining = response.headers.get('X-RateLimit-Remaining')
        rate_reset = response.headers.get('X-RateLimit-Reset')

        if token is None:
            print("\nSome information may not be present as you have not entered an access token!")

        print("\nRate Limit Information:")
        print(f"Rate Limit: {rate_limit} requests per hour")
        print(f"Remaining Requests: {rate_remaining} requests left")
        print(f"Rate Limit Reset at: {rate_reset}")

        try:
            if input("\nWould you like to save this in a .json file? (y/n): ").lower() == "y":
                with open("API-Output.json", "w") as f:
                    json.dump(data, f, indent=4)

        except PermissionError as e:
            print("\nYou dont have the permission to create a file in this directory.")
            print(f"{Fore.RED}{type(e).__name__}: {Fore.WHITE}{e}")

    else:
        print(f"Error: {response.status_code}")
        print(f"More informations under: {GitHub_RESTAPI_docs}")

# Error handeling for unexpected errors as I often do silly mistakes
except Exception as e:
    print(f"\n{Fore.RED}An unexpected error occurred:")
    print(f"{type(e).__name__}: {e}")
    print("\nPlease report this issue with the above error message on GitHub 'Akeoots/GitHub-Activity-Fetcher/issues'.")

input("\nPress Enter To Exit...")
sys.exit()