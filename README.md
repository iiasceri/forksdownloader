
# ForksDownloader

The ForksDownloader project is a utility for cloning all forks of a GitHub repository and merging them into the original repository. This project is useful for developers who want to review or archive all the modifications made in the forks of a specific repository.

## Components

The project contains the following main components:

1. `downloadforks.py`: This Python script uses the GitHub API to clone all forks of a specified repository.

2. `mergeforks.py`: This Python script merges all the cloned forks into the master branch of the original repository.

3. `downloadforks.sh`: This Shell script is a utility to execute the `downloadforks.py` script.

4. `requirements.txt`: This file lists the Python dependencies required to run the project.

5. `github_fork_cloner_guide.md`: This markdown file contains instructions for using the `downloadforks.py` script.

## Setup

1. Install Python 3.6 or higher.

2. Install the Python dependencies listed in `requirements.txt` by running `pip install -r requirements.txt`.

3. Generate a GitHub personal access token from your GitHub account settings. The token needs the `public_repo` or `repo` (for private repositories) scope.

## Usage

### Cloning Forks

To clone all forks of a repository, run the `downloadforks.py` script with the required arguments. For example:

```shell
python downloadforks.py -owner JesusFreke -repo smalidea -token YOUR_GITHUB_TOKEN
```

This will clone all forks of the `smalidea` repository owned by `JesusFreke`. Each fork will be cloned into a new subdirectory in the current directory. The name of the subdirectory will be `fork<i>`, where `<i>` is the index of the fork.

If you want to clone only forks that are active in the last 6 months, add the `-onlyactive` flag:

```shell
python downloadforks.py -owner JesusFreke -repo smalidea -onlyactive -token YOUR_GITHUB_TOKEN
```

### Merging Forks

To merge all the cloned forks into the original repository, run the `mergeforks.py` script with the name of the repository as an argument. For example:

```shell
python mergeforks.py smalidea
```

This will merge all the forks into the master branch of the `smalidea` repository. The result will be in a new directory named `all_merged_into_original`.

## Note

Please remember to respect the terms of use of the GitHub API and the data you download. You should not use this script to download large amounts of data or to violate the privacy or intellectual property rights of others.
