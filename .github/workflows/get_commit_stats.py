import requests
from requests.auth import HTTPBasicAuth
import os

username = os.getenv('GITHUB_USERNAME')
token = os.getenv('GITHUB_TOKEN')

def get_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url, auth=HTTPBasicAuth(username, token))
    repos = response.json()
    return [repo['name'] for repo in repos]

def get_commits(username, repo):
    url = f'https://api.github.com/repos/{username}/{repo}/commits'
    response = requests.get(url, auth=HTTPBasicAuth(username, token))
    commits = response.json()
    return commits

def main(username):
    repos = get_repos(username)
    total_commits = 0

    for repo in repos:
        commits = get_commits(username, repo)
        for commit in commits:
            if commit['commit']['author']['name'] == username:
                total_commits += 1

    with open('commit_stats.txt', 'w') as f:
        f.write(f'Total commits: {total_commits}')

if __name__ == '__main__':
    main(username)