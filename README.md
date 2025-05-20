# GitHub Activity Fetcher

A lightweight Python tool that allows you to fetch and view GitHub user activity, either from their general profile or scoped to a specific repository. It uses the GitHub REST API v3 and supports optional or required token-based authentication depending on your query.

---

## 🧠 Features

- Fetches:
  - A user's **general public activity** (`/users/<username>/events`)
  - A user's **repo-specific activity** (`/repos/<username>/<repo>/events`)
- Allows logging program events
- Provides **rate limit feedback** after each request
- Pretty-prints structured event data
- Allows **JSON saving** of fetched data (with overwrite and fallback directory support)
- Includes simple CLI input flow and graceful exit handling
- Designed with `customtkinter` and `PyQt5`

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

You'll also provide a GitHub username, optional/requisite token and a User-Agent header.

After fetching:
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

This program is **released as an executable**, but if you’re on Linux or are a dev you may need to run the source code:

1. **Ensure Python 3 is installed.** You can verify with:
   ```bash
   python3 --version
   ```
   If Python 3 is not installed, install it via your package manager (e.g., `sudo apt install python3`).

2. **Install all the required modules** if it’s not installed already:

   Functional:
       `os`
       `sys`
       `time`
       `json`
       `logging`
       `requests`

   Visual:
       `PyQt5`
       `pprint`
       `ctypes`
       `tkinter`
       `customtkinter`

3. **Run the program directly** from the source code of the selected tag aka version:
   - [All tags aka version](https://github.com/Akeoottt/GitHub-Activity-Fetcher/tags)
   
This will allow you to interact with the program as expected. Make sure to follow the prompts to fetch GitHub activity.

---

## ✨ Credit

- Terminal coloring uses ANSI sequences. special thanks to `CosmicBit128` for reference styling and code review
- Developed by **Akeoott**