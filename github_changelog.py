# Get the changelog from a specified git repository from a specified committer date using github API

# import modules
import os
import sys
import json
import requests
import argparse
import datetime

# define variables
GITHUB_API_URL = 'https://api.github.com'
GITHUB_API_HEADERS = {'Accept': 'application/vnd.github.v3+json'}
GITHUB_API_PARAMS = {'per_page': 100}

# define functions
def get_commits(repo, start_date, end_date):
    """
    Get the commits from a specified repository from a specified committer date
    """
    # get the commits from the repository
    commits = []
    url = GITHUB_API_URL + '/repos/' + repo + '/commits'
    params = GITHUB_API_PARAMS.copy()
    params['since'] = start_date
    params['until'] = end_date
    while True:
        response = requests.get(url, params=params, headers=GITHUB_API_HEADERS)
        if response.status_code == 200:
            commits.extend(response.json())
            if response.links.get('next'):
                url = response.links['next']['url']
            else:
                break
        else:
            print('Error:', response.status_code, response.reason)
            break
    return commits

# define main function
def main():
    """
    Get the changelog from a specified git repository from a specified committer date using github API
    """
    # parse the arguments
    parser = argparse.ArgumentParser(description='Get the changelog from a specified git repository from a specified committer date using github API')
    parser.add_argument('-r', '--repo', help='the repository name', required=True)
    parser.add_argument('-s', '--start', help='the start date', required=True)
    parser.add_argument('-e', '--end', help='the end date', required=True)
    args = parser.parse_args()

    # get the commits from the repository
    commits = get_commits(args.repo, args.start, args.end)

    # get the commits from the repository, number the commits and write the changelog to the file
    commits_number = 1
    with open('changelog.md', 'w') as changelog:
        changelog.write('# Changelog\n\n')
        for commit in commits:
            changelog.write('## ' + str(commits_number) + '. ' + commit['commit']['message'].split('\n')[0] + '\n\n')
            changelog.write('- ### Author: ' + commit['commit']['author']['name'] + '\n')
            changelog.write('- ### Date Authored: ' + commit['commit']['author']['date'] + '\n')
            changelog.write('- ### Committer: ' + commit['commit']['committer']['name']+ '\n')
            changelog.write('- ### Date Committed: ' + commit['commit']['committer']['date']+ '\n')
            commits_number += 1


# run the main function
if __name__ == '__main__':
    main()

# end of github_changelog.py
