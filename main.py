import requests, sys

while True:
    username = input("Whats the username of the person you want to fetch from: ")
    url = f'https://api.github.com/users/{username}/events'

    UserAgent = input('Enter your app name or identifier: ')
    while True:
        token = input('Optional -> Enter your personal access token. If not, enter "no" (case sensitive): ')
        if token == "no":
            token = None
        break
    break

print(f"\nIs this correct?\nUsername: {username}\nApp name or identifier: {UserAgent}\nYour token: {token}\n")
if token is None:
    print("(Your token is None, its because you either have entered it wrong or you didnt want to enter one)\n")

while True:
    confirm = input("Do you want to continue? (y/n): ").lower()
    print()
    if confirm == "y":
        break
    else:
        sys.exit()

headers = {
    'User-Agent': UserAgent,
    'Accept': 'application/vnd.github.v3+json'
}

if token:
    headers['Authorization'] = f'token {token}'

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    print("\nUser Events:", data)
    
    rate_limit = response.headers.get('X-RateLimit-Limit')
    rate_remaining = response.headers.get('X-RateLimit-Remaining')
    rate_reset = response.headers.get('X-RateLimit-Reset')
    
    if token is None:
        print("\nSome information may not be present as you have not entered an API key!")

    print("\nRate Limit Information:")
    print(f"Rate Limit: {rate_limit} requests per hour")
    print(f"Remaining Requests: {rate_remaining} requests left")
    print(f"Rate Limit Reset at: {rate_reset}")
else:
    print(f"Error: {response.status_code}")