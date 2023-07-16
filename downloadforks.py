import asyncio
import aiohttp
import argparse
import shutil
import os
from dateutil.parser import parse as parse_date
from datetime import datetime, timedelta, timezone

# Create the parser
parser = argparse.ArgumentParser(description='Clone all forks of a GitHub repo.')
parser.add_argument('-owner', type=str, required=True, help='The owner of the repo')
parser.add_argument('-repo', type=str, required=True, help='The name of the repo')
parser.add_argument('-onlyactive', action='store_true', help='Only clone forks active in the last 6 months')
parser.add_argument('-token', type=str, required=True, help='The GitHub personal access token')

# Parse the arguments
args = parser.parse_args()

# Header for GitHub API
headers = {
    "Authorization": f"token {args.token}",
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


# A coroutine function to clone a fork asynchronously
async def clone_fork(session, fork, i):
    if args.onlyactive:
        six_months_ago = datetime.now(timezone.utc) - timedelta(days=6 * 30)
        if parse_date(fork['pushed_at']) <= six_months_ago:
            return  # Skip inactive fork
    subprocess = await asyncio.create_subprocess_shell(f"git clone {fork['clone_url']} fork{i}")  # Run git clone in a subprocess
    await subprocess.wait()  # Wait for the subprocess to finish

    # Create a redirect HTML file in the fork directory
    with open(f"fork{i}/gotorepo.html", "w") as f:
        f.write(f'''<html>
<head>
<meta http-equiv="refresh" content="0; URL={fork['html_url']}" />
</head>
<body>
</body>
</html>''')


# A coroutine function to get and clone all forks asynchronously
async def get_and_clone_forks():
    page = 1
    tasks = []  # A list of tasks to await
    async with aiohttp.ClientSession(headers=headers) as session:  # Create a session for HTTP requests

        # Clone the original repository asynchronously
        subprocess = await asyncio.create_subprocess_shell(f"git clone https://github.com/{owner}/{repo}.git {repo}_original")
        await subprocess.wait()  # Wait for the subprocess to finish

        # Create a redirect HTML file in the original repository directory
        try:
            with open(f"{repo}_original/gotorepo.html", "w") as f:
                f.write(f'''<html>
<head>
<meta http-equiv="refresh" content="0; URL=https://github.com/{owner}/{repo}" />
</head>
<body>
</body>
</html>''')
        except FileNotFoundError:
            print(f"Could not write to {repo}_original/gotorepo.html. The directory may not exist yet.")

        while True:
            response = await session.get(
                f"https://api.github.com/repos/{owner}/{repo}/forks?page={page}&per_page=100")  # Get the list of forks asynchronously
            response.raise_for_status()
            forks = await response.json()  # Parse the JSON response asynchronously
            if not forks:  # If the list is empty, we've reached the end of the forks
                break
            # Create a task for each fork to clone it asynchronously and add it to the list of tasks
            for i, fork in enumerate(forks, start=(page - 1) * 100 + 1):
                tasks.append(asyncio.create_task(clone_fork(session, fork, i)))
            page += 1  # Go to the next page
        await asyncio.gather(*tasks)  # Wait for all tasks to finish


# Run the main coroutine function
asyncio.run(get_and_clone_forks())