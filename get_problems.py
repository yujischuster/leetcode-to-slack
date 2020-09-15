import requests
import json

response = requests.get("https://leetcode.com/api/problems/algorithms/")
data = json.loads(response.content)

for problem in range(len(data["stat_status_pairs"])):
    if not data["stat_status_pairs"][problem]["paid_only"]:
        print(data["stat_status_pairs"][problem]["stat"]["question__title_slug"])

