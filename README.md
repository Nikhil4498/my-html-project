# step-by-step procedure to set up a complete CI/CD pipeline using Bash, Python, and cron on an EC2 instance.


# Step 1: Set Up a Simple HTML Project

Create a simple HTML project:
On your local machine, create a directory for the project:

mkdir my-html-project
cd my-html-project

Add an index.html file:

html
Copy code
<!DOCTYPE html>
<html>
<head>
    <title>My HTML Project</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>

# Initialize a Git repository:

git init
git add .
git commit -m "Initial commit"

# Push the project to GitHub:
Create a repository on GitHub.
Push your code:

git remote add origin <your-repo-url>
git branch -M main
git push -u origin main

# Step 2: Set Up AWS EC2 Instance with Nginx
Connect to your EC2 instance via SSH:


ssh -i "your-key.pem" ec2-user@<your-ec2-public-ip>
Install Nginx:

sudo apt update
sudo apt install nginx -y

Configure Nginx to serve your HTML project:

Create a new configuration file:

sudo nano /etc/nginx/sites-available/html-project

Add the following Nginx configuration:

server {
    listen 80;
    server_name <your-ec2-public-ip>;

    location / {
        root /var/www/html/my-html-project;
        index index.html;
    }
}

Link the configuration and restart Nginx:

sudo ln -s /etc/nginx/sites-available/html-project /etc/nginx/sites-enabled/
sudo systemctl restart nginx

Clone your HTML project to /var/www/html:

sudo git clone https://github.com/<your-username>/<your-repo>.git /var/www/html/my-html-project

# Step 3: Write a Python Script to Check for New Commits

Create the Python script:

On EC2 instance, create a script to check for new commits from GitHub:

nano check_commits.py

Add the following code:

import requests
import os

GITHUB_REPO = "https://api.github.com/repos/<your-username>/<your-repo>/commits"
LOCAL_FILE = "/var/www/html/my-html-project/.git/refs/heads/main"

def get_latest_commit():
    response = requests.get(GITHUB_REPO)
    if response.status_code == 200:
        return response.json()[0]['sha']
    return None

def get_local_commit():
    with open(LOCAL_FILE, 'r') as f:
        return f.read().strip()

def check_for_new_commit():
    latest_commit = get_latest_commit()
    local_commit = get_local_commit()

    if latest_commit != local_commit:
        os.system('bash deploy_code.sh')

if __name__ == "__main__":
    check_for_new_commit()
    
Save and exit the file.

Install required libraries:

sudo apt install python3-pip
pip3 install requests

# Step 4: Write a Bash Script to Deploy the Code

Create the Bash deployment script:
In  EC2 instance, create a deployment script:

nano deploy_code.sh

Add the following code:

#!/bin/bash
cd /var/www/html/my-html-project
git pull origin main
sudo systemctl restart nginx

Save the file and make it executable:

chmod +x deploy_code.sh

# Step 5: Set Up a Cron Job to Run the Python Script
Open the cron editor:

crontab -e

Add the following entry to check for new commits every minute:

* * * * * /usr/bin/python3 /home/ec2-user/check_commits.py
        * 
This will run the Python script every minute to check for new commits.

# Step 6: Test the Setup

Make a new commit to your GitHub repository:

On your local machine, make changes to index.html, for example:
html
Copy code
<h1>Hello, World! CI/CD is working!</h1>

Commit and push the changes:

git add .
git commit -m "Updated index.html"
git push origin main
Verify the changes on  EC2 instance:

After a minute, visit  EC2 public IP in the browser. You should see the updated changes without manually deploying.
