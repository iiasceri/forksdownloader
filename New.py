import requests
import subprocess
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Clone all forks of a GitHub repo.')
parser.add_argument('-owner', type=str, required=True, help='The owner of the repo')
parser.add_argument('-repo', type=str, required=True, help='The name of the repo')

# Parse the arguments
args = parser.parse_args()

# Replace with your token
token = "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"

# Header for GitHub API
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
}

# The repository to clone
owner = args.owner
repo = args.repo

# Clone the original repository
subprocess.run(["git", "clone", f"https://github.com/{owner}/{repo}.git", f"{repo}_original"])

# Get the list of forks
response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/forks", headers=headers)
response.raise_for_status()
forks = response.json()

# Clone each fork into a separate directory
for i, fork in enumerate(forks, start=1):
    subprocess.run(["git", "clone", fork["clone_url"], f"fork{i}"])
