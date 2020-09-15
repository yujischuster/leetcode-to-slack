import requests
import json
import os
from slack import WebClient
from slack.errors import SlackApiError
import schedule
import time

response = requests.get("https://leetcode.com/api/problems/algorithms/")
data = json.loads(response.content)

def post_problem(problem):
    webhook_url = 'https://hooks.slack.com/services/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'
    output = { "text": "https://leetcode.com/problems/" + problem }
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

for problem in range(len(data["stat_status_pairs"])):
    if not data["stat_status_pairs"][problem]["paid_only"]:
        while True:
            schedule.run_pending()
            time.sleep(1)
        
        problem_slug = data["stat_status_pairs"][problem]["stat"]["question__title_slug"]
        schedule.every().tuesday.at("17:00").do(post_problem(problem_slug))
        print("posted")