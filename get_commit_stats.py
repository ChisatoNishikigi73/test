import requests
from requests.auth import HTTPBasicAuth
import os
import sys

username = os.getenv('GITHUB_USERNAME')
token = os.getenv('GITHUB_TOKEN')

def get_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url, auth=HTTPBasicAuth(username, token))
    response.raise_for_status()
    repos = response.json()
    return [repo['name'] for repo in repos]

def get_commits(username, repo):
    url = f'https://api.github.com/repos/{username}/{repo}/commits'
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, token))
        response.raise_for_status()
        commits = response.json()
        return commits
    except requests.exceptions.HTTPError as e:
        print(f"警告：无法访问仓库 {repo}：{e}")
        return []

def main(username):
    if not username:
        print("错误：GitHub用户名未设置。请设置GITHUB_USERNAME环境变量。")
        sys.exit(1)
    
    if not token:
        print("错误：GitHub令牌未设置。请设置GITHUB_TOKEN环境变量。")
        sys.exit(1)

    try:
        repos = get_repos(username)
        total_commits = 0
        accessible_repos = 0

        for repo in repos:
            commits = get_commits(username, repo)
            if commits:
                accessible_repos += 1
                for commit in commits:
                    if commit['commit']['author']['name'] == username:
                        total_commits += 1

        with open('commit_stats.txt', 'w') as f:
            f.write(f'总提交次数: {total_commits}\n')
            f.write(f'可访问仓库数: {accessible_repos}/{len(repos)}')
        
        print(f"统计完成。总提交次数：{total_commits}")
        print(f"可访问仓库数：{accessible_repos}/{len(repos)}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误：{e}")
        print("请确保您的GitHub用户名和令牌正确，并且有足够的权限访问这些仓库。")
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == '__main__':
    print(f"使用的用户名: {username}")
    print(f"令牌是否设置: {bool(token)}")
    main(username)