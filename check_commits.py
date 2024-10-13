import requests
import os
import sys

# GitHub repository details
REPO_OWNER = 'Nikhil4498'
REPO_NAME = 'my-html-project'
GITHUB_API_URL = f'https://api.github.com/repos/Nikhil4498/my-html-project/commits'

# File to store the last commit SHA
LAST_COMMIT_FILE = '/home/ec2-user/last_commit.txt'

def get_latest_commit():
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        commits = response.json()
        return commits[0]['sha']
    else:
        print(f"Failed to fetch commits: {response.status_code}")
        return None

def get_stored_commit():
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, 'r') as f:
            return f.read().strip()
    return None

def update_stored_commit(sha):
    with open(LAST_COMMIT_FILE, 'w') as f:
        f.write(sha)

def main():
    latest_commit = get_latest_commit()
    if not latest_commit:
        sys.exit(1)
    stored_commit = get_stored_commit()
    if latest_commit != stored_commit:
        print("New changes detected")
        update_stored_commit(latest_commit)
        sys.exit(0)
    else:
        print("No new changes")
        sys.exit(1)

if __name__ == "__main__":
    main()
