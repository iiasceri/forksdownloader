import requests
import subprocess
import argparse
import shutil
import os
from dateutil.parser import parse as parse_date
from datetime import datetime, timedelta, timezone

# Replace with your token
token = "YOUR_GITHUB_TOKEN"

# Create the parser
parser = argparse.ArgumentParser(description='Clone all forks of a GitHub repo.')
parser.add_argument('-owner', type=str, required=True, help='The owner of the repo')
parser.add_argument('-repo', type=str, required=True, help='The name of the repo')
parser.add_argument('-onlyactive', action='store_true', help='Only clone forks active in the last 6 months')

# Parse the arguments
args = parser.parse_args()

# Header for GitHub API
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
}

# The repository to clone
owner = args.owner
repo = args.repo

# Clean up any existing directories from previous runs
if os.path.exists(f"{repo}_original"):
    shutil.rmtree(f"{repo}_original")
for i in range(1, 101):  # assuming maximum 100 forks for simplicity
    if os.path.exists(f"fork{i}"):
        shutil.rmtree(f"fork{i}")

# Clone the original repository
subprocess.run(["git", "clone", f"https://github.com/{owner}/{repo}.git", f"{repo}_original"])

# Create a redirect HTML file in the original repository directory
with open(f"{repo}_original/gotorepo.html", "w") as f:
    f.write(f'''<html>
<head>
<meta http-equiv="refresh" content="0; URL=https://github.com/{owner}/{repo}" />
</head>
<body>
</body>
</html>''')

# Get the list of forks
page = 1
while True:
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/forks?page={page}&per_page=100", headers=headers)
    response.raise_for_status()
    forks = response.json()
    if not forks:  # If the list is empty, we've reached the end of the forks
        break
    # Clone each fork into a separate directory
    for i, fork in enumerate(forks, start=(page - 1) * 100 + 1):
        if args.onlyactive:
            six_months_ago = datetime.now(timezone.utc) - timedelta(days=6*30)
            if parse_date(fork['pushed_at']) <= six_months_ago:
                continue  # Skip inactive fork
        subprocess.run(["git", "clone", fork["clone_url"], f"fork{i}"])

        # Create a redirect HTML file in the fork directory
        with open(f"fork{i}/gotorepo.html", "w") as f:
            f.write(f'''<html>
<head>
<meta http-equiv="refresh" content="0; URL={fork["html_url"]}" />
</head>
<body>
</body>
</html>''')
    page += 1  # Go to the next page