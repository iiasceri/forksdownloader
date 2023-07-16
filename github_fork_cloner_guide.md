
# GitHub Fork Cloner

This Python script uses the GitHub API to clone all forks of a given repository. It requires two command-line arguments: `-owner` and `-repo`, which specify the owner and the name of the repository, respectively.

## Requirements

- Python 3.6 or higher
- `requests` library
- A GitHub personal access token

## Setup

1. Make sure Python 3 is installed on your machine. You can download Python from the [official website](https://www.python.org/downloads/).
2. Install the `requests` library if you haven't already. You can install it using pip:
   ```shell
   pip install requests
   ```
3. Generate a new GitHub personal access token. You can do this in your GitHub account settings. The token needs the `public_repo` or `repo` (for private repositories) scope.
4. Replace `YOUR_GITHUB_TOKEN` in the script with your personal access token.

## Usage

Run the script from the command line, specifying the `-owner` and `-repo` arguments. For example, to clone all forks of the `smalidea` repository owned by `JesusFreke`, you would run:

```shell
python script.py -owner JesusFreke -repo smalidea
```

The script will clone each fork into a new subdirectory in the current directory. The name of the subdirectory will be the name of the fork.

## Note

Please remember to respect the terms of use of the GitHub API and the data you download. You should not use this script to download large amounts of data or to violate the privacy or intellectual property rights of others.
