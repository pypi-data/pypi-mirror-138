import logging
import os
from json import load, loads
from subprocess import check_output
from requests import post

from ocs.args import args
from ocs.languages import languages


# TODO: Run this code every time the data changes
# Store data about server, contests, and problems
about_data = {'version': '2.6', 'languages': {}, 'contests': []}
contest_data = {}
problem_data = {}


# Get language versions
for name, description in languages.items():
    about_data['languages'][name] = check_output(description.version, shell=True).decode('utf-8')[:-1]


# Save information
for contest in os.listdir(args.contests_dir):
    about_data['contests'].append(contest)
    contest_data[contest] = load(open(os.path.join(args.contests_dir, contest, 'info.json'), 'r'))
    problem_data[contest] = {}
    for problem in contest_data[contest]['problems']:
        if ' ' not in problem:
            # Local problem
            problem_data[contest][problem] = load(open(os.path.join(
                args.contests_dir, contest, problem, 'info.json'), 'r'))
        else:
            # Federated problem
            fed_problem, fed_contest, server = problem.split()
            problem_data[contest][problem] = loads(post(('https://' if server.find('://') == -1 else '') + server, json={
                'type': 'info', 'contest': fed_contest, 'problem': fed_problem}).text)


# Log data
logging.debug(about_data)
logging.debug(contest_data)
logging.debug(problem_data)
