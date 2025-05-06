# GitHub Activity Fetcher

A lightweight Python tool that allows you to fetch and view GitHub user activity, either from their general profile or scoped to a specific repository. It uses the GitHub REST API v3 and supports optional or required token-based authentication depending on your query.

---

## 🧠 Features

- Fetches:
  - A user's **general public activity** (`/users/<username>/events`)
  - A user's **repo-specific activity** (`/repos/<username>/<repo>/events`)
- Provides **rate limit feedback** after each request
- Pretty-prints structured event data
- Allows **JSON saving** of fetched data (with overwrite and fallback directory support)
- Includes simple CLI input flow and graceful exit handling
- Designed with basic theming and color-coded prompts for better UX

---

## 📦 Structure Overview

| Function | Purpose |
|---------|---------|
| `user_input()` | Interactive CLI that gathers parameters such as username, repo name, user-agent, and token |
| `api_request()` | Constructs and sends the appropriate GitHub API request |
| `response_parsing()` | *(Merged with api_request)* Decodes JSON and checks for HTTP issues |
| `output_formatting()` | Displays the received data in readable form and prints rate limits |
| `data_saving()` | Optionally saves JSON output to disk, with fallback path support |

---

## 🔐 Authentication Info

- **General user events**: token is *optional*
- **Repo-specific events**: token is *required*

You can generate a token by following GitHub's guide:  
👉 [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

---

## 🚀 Usage

Run the executable

You will be prompted to choose between:
1. General user activity
2. Repo-specific activity

You'll also provide a GitHub username, optional/requisite token, and an application name (used in the User-Agent header).

After fetching:
- Event data is printed to the console
- You'll be asked if you want to save the output to a JSON file

---

## 🧪 Known Limitations

- This project is **fresh** and may contain bugs or edge cases not yet handled
- Only public data is accessible
- Rate limiting applies, especially without a token

If you encounter any issues, feel free to open an issue on [Akeoots/GitHub-Activity-Fetcher](https://github.com/Akeoots/GitHub-Activity-Fetcher/issues)

---

## 📁 Output Example

```json
[
  {
    "type": "PushEvent",
    "actor": { "login": "example-user", ... },
    "repo": { "name": "example-user/example-repo", ... },
    ...
  }
]
```

You’ll also get this info after each request:
- Remaining API requests
- Reset time for rate limit
- Total rate limit cap

---

## 🐧 For Linux Users and developers

This program is **released as an executable**, but if you’re on Linux or are a dev and need to run the source code:

1. **Ensure Python 3 is installed.** You can verify with:
   ```bash
   python3 --version
   ```
   If Python 3 is not installed, install it via your package manager (e.g., `sudo apt install python3`).

2. **Install the `requests` module** if it’s not installed already:
   ```bash
   pip3 install requests
   ```

3. **Run the program directly** from the source code of the archived versions or run the latest update:
   * [Archived versions](https://github.com/Akeoottt/GitHub-Activity-Fetcher/tree/main/archive/source-code)
     * v1.2.1.py
     * v1.2.0.py
   * [Most recent update](https://github.com/Akeoottt/GitHub-Activity-Fetcher/blob/main/main.py)
     * main.py
   

This will allow you to interact with the program as expected. Make sure to follow the prompts to fetch GitHub activity.

---

## ✨ Credit

- Terminal coloring uses ANSI sequences; special thanks to `CosmicBit128` for reference styling and code review
- Developed by **Akeoott**

https://roadmap.sh/projects/github-user-activity
