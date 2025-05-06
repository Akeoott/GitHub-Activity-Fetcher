from input_handler import UserInputHandler
from github_client import GitHubAPIClient
from data_handler import DataHandler
import sys

def main():
    try:
        input_handler = UserInputHandler()
        endpoint, username, useragent, token = input_handler.prompt()

        client = GitHubAPIClient(endpoint, username, useragent, token)
        data, (limit, remaining, reset) = client.fetch_events()

        handler = DataHandler(username, token)
        handler.display(data, limit, remaining, reset)
        handler.save(data)

    except Exception as e:
        print(f"\n\033[91mUnexpected error:\033[0m")
        print(f"\033[91m{type(e).__name__}:\033[0m {e}")
        print("\nPlease report this issue on GitHub 'Akeoots/GitHub-Activity-Fetcher/issues'")

    input("\nPress Enter To Exit...")
    sys.exit()

if __name__ == "__main__":
    main()