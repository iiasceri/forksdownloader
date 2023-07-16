import os
import subprocess
import shutil

# Get the repo name from the command line argument
import sys
repo = sys.argv[1]

# Clean up any existing directories from previous runs
if os.path.exists("all_merged_into_original"):
    shutil.rmtree("all_merged_into_original")

# Find the original repository folder name
original = None
for d in os.listdir("."):
    print(d)
    if d.endswith(f"{repo}_original"):
        original = d
        break

# Copy the original repository to a new directory
print(original)
shutil.copytree(original, "all_merged_into_original")

# Get the list of fork directories
forks = [d for d in os.listdir(".") if d.startswith("fork")]

# Change the current working directory to the new directory
os.chdir("all_merged_into_original")

# Add all the forks as remote repositories
for fork in forks:
    subprocess.run(["git", "remote", "add", fork, f"../{fork}"])

# Fetch all the remote branches
subprocess.run(["git", "fetch", "--all"])

# Merge all the forks into the master branch of the original repository
for fork in forks:
    # Use -m option to specify the commit message as "bla"
    subprocess.run(["git", "merge", "-X", "ours", "-m", "bla", f"{fork}/master"])
