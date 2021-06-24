#!/usr/bin/python3
# Script created to conduct Security Audits on Github.
#
# First version: 2020-04-17
# Owner/Contact: Marcus Burghardt - https://github.com/marcusburghardt

# References:
# - https://developer.github.com/v3/
# - https://developer.github.com/v3/libraries/
# - https://github.com/PyGithub/PyGithub
# - sudo pip3 install PyGithub

import argparse
parser = argparse.ArgumentParser(description='Get Github Information.')
parser.add_argument('-o', '--org', action='store', default='ExampleOrg',
                    help='Inform the organization ID (login property) to be consulted.')
parser.add_argument('-f', '--function', action='store', default='repos',
                    help='Script function. repo, repos, members, events, repo_events, member_events and user_events.')
parser.add_argument('-r', '--repository', action='store', default='all',
                    help='Repo name.')
parser.add_argument('-u', '--user', action='store', default='all',
                    help='User whose the information will be consulted.')
parser.add_argument('-csv', '--csv', action='store_true',
                    help='Output in CSV format.')
parser.add_argument('-c', '--count', action='store_true',
                    help='Show the numbers only.')
parser.add_argument('-d', '--discovery', action='store_true',
                    help='Used to a JSON output compatible with Zabbix Discovery Rules.')

args = parser.parse_args()
ORG = args.org
FUNCTION = args.function
REPOSITORY = args.repository
USER = args.user

# Adjust the environment appropriately.
# Info for authentication (sensitive data)
CREDS_FILE='CHANGE_ME'

import configparser
config = configparser.ConfigParser()
config.read(CREDS_FILE)
config.sections()
token = config['DEFAULT']['token']

from github import Github
g = Github(token)

# Used for counting and generic printing
def print_results(results,objectType):
    if args.count:
        print(results.totalCount)
        exit()
    firstLine = True
    for item in results:
        if objectType == 'repository':
            if firstLine:
                print('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % ('repoName', 'repoFullName', 'repoId', 'repoUrl',
                                                                     'private', 'owner', 'ownerUrl', 'forks_count', 
                                                                     'watchers_count', 'open_issues_count', 'subscribers_count', 
                                                                     'created_at', 'pushed_at', 'updated_at', 'private'))
                firstLine = False
            print('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (item.name, item.full_name, item.id, item.html_url,
                                                                 item.private, item.owner.login, item.owner.html_url, item.forks_count,
                                                                 item.watchers_count, item.open_issues_count, item.subscribers_count,
                                                                 item.created_at, item.pushed_at, item.updated_at, item.private))
            continue
        if objectType == 'user':
            try:
                membership = item.get_organization_membership(ORG)
                if firstLine:
                    print('%s,%s,%s,%s,%s,%s,%s' % ('user', 'name', 'email', 'userUrl',
                                                    'membershipState', 'organization', 'organizationRole'))
                    firstLine = False
                print('%s,%s,%s,%s,%s,%s,%s' % (item.login, membership.user.name, membership.user.email, membership.user.url,
                                            membership.state, membership.organization.login, membership.role))
            except:
                print('%s,%s' % (item.login, item.html_url))
            continue
        else:
            print(item)

def repo_events(repo):
    events = repo.get_events()
    if args.count and not args.csv:
        print('%s,%s' % (repo.name,events.totalCount))
    for event in events:
        print('%s,%s,%s,%s,%s' % (repo.organization.login, repo.name, event.actor.login, event.type, event.created_at))

def user_events(member):
    events = member.get_events()
    if args.count and not args.csv:
        print('%s,%s' % (member.name,events.totalCount))
    for event in events:
        if event.org:
            organization = event.org.login
        else:
            organization = 'None'
        print('%s,%s,%s,%s,%s' % (event.actor.login, organization, event.repo.name, event.type, event.created_at))

# Don't use this function for big organizations, as it can reach the API limit.
def member_events(repos,members):
    if args.count:
        print('%s,%s,%s,%s,%s,%s,%s' % ('user', 'userUrl', 'membershipState', 
                                        'organization', 'organizationRole',
                                        'repoName', 'repoActivities'))
    else:
        print('%s,%s,%s,%s' % ('user', 'repoName', 'eventType', 'eventCreated'))
    for repo in repos:
        events = repo.get_events()
        for member in members:
            count = 0
            for event in events:
                event_user = event.actor.login
                if event_user in member.login:
                    if args.count:
                        count += 1
                        continue
                    else:
                        print('%s,%s,%s,%s' % (event_user, event.repo.name, event.type, event.created_at))
            if args.count:
                membership = member.get_organization_membership(ORG)
                print('%s,%s,%s,%s,%s,%s,%s' % (member.login, membership.user.url, membership.state, 
                                                membership.organization.login, membership.role,
                                                repo.name, count))

def run_discovery(results):
    import json
    import sys
    # Starts the array.
    data = {}
    data['data'] = []
    for item in results: 
        data['data'].append({
            '{#GITHUB_REPO_FULLNAME}': item.full_name, '{#GITHUB_REPO_TITLE}': item.name,
        })
     # Print the results in JASON format.
    json.dump(data, sys.stdout)
    exit()

def main():
    # Check an specif repository via its full_name or id.
    # I am printing only information considered relevant to be monitored.
    if FUNCTION == 'repo':
        try:
            repo = g.get_repo(REPOSITORY)
            events = repo.get_events()
            if args.csv:
                print('%s,%s,%s,%s,%s,%s,%s' % ('forks_count', 'watchers_count', 'subscribers_count',
                                                'open_issues_count', 'private', 'events',
                                                'updated_at'))
            print('%s,%s,%s,%s,%s,%s,%s' % (repo.forks_count, repo.watchers_count, repo.subscribers_count,
                                            repo.open_issues_count, repo.private, events.totalCount,
                                            repo.updated_at))
        except:
            print('Repository not found!')
    # user_events is not limited to organization members.       
    elif FUNCTION == 'user_events':
        try:
            user = g.get_user(login=USER)
            user_events(user)
        except:
            print('User not found!')
    else:
        # All other functions work inside the organization scope.
        org = g.get_organization(ORG)

    if args.discovery:
        results = org.get_repos()
        run_discovery(results)

    if FUNCTION == 'repos':
        results = org.get_repos(type=REPOSITORY)
        print_results(results,'repository')
    elif FUNCTION == 'members':
        results = org.get_members(role=REPOSITORY)
        print_results(results,'user')
    elif FUNCTION == 'outsiders':
        results = org.get_outside_collaborators()
        print_results(results,'user')
    # Only public events supported by ORG.
    # For details it is recommended to use the repo_events function.
    elif FUNCTION == 'events':
        results = org.get_events()
        print_results(results,None)
    elif FUNCTION == 'repo_events':
        if args.csv:
            print('%s,%s,%s,%s,%s' % ('organization', 'repository', 'user', 'eventType', 'created_at'))
        if REPOSITORY != 'all':
            repo_events(org.get_repo(REPOSITORY))
        else:
            repos = org.get_repos()
            for repo in repos:
                repo_events(repo)
    elif FUNCTION == 'member_events':
        members = org.get_members()
        repos = org.get_repos()
        member_events(repos,members)

if __name__ == '__main__':
    main()