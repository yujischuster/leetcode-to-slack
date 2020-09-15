import requests
import json
import os
from slack import WebClient
from slack.errors import SlackApiError
import schedule
import time
from random import randrange

def post_problem(all_problems):
    slug = all_problems[randrange(len(all_problems))]  # choose random problem
    webhook_url = ""
    output = { "text": "This week's warm-up problem: " + "https://leetcode.com/problems/" + slug }
    # post
    slack_response = requests.post(
        webhook_url, data=json.dumps(output),
        headers={'Content-Type': 'application/json'}
    )
    if slack_response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (slack_response.status_code, slack_response.text)
        )

# get data
response = requests.get("https://leetcode.com/api/problems/algorithms/")
data = json.loads(response.content)

# filter-out premium ones, get slugs
all_problems = []
for problem in range(len(data["stat_status_pairs"])):
    if not data["stat_status_pairs"][problem]["paid_only"]:
        single_problem = data["stat_status_pairs"][problem]["stat"]["question__title_slug"]
        all_problems.append(single_problem)

# schedule job
schedule.every().monday.at("10:00").do(post_problem, all_problems)

while True:
    schedule.run_pending()
    time.sleep(1)