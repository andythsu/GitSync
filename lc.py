import os

import requests

from lc_queries import get_problem_set_question_list_query, get_submission_details_query, get_submission_list_query

class LCApi:
    def __init__(self):
      self.lc_session = os.environ.get("LEETCODE_SESSION", "")
      self.host = "https://leetcode.com/graphql"
      self.headers = {
         "Cookie": f"LEETCODE_SESSION=\"{self.lc_session}\"",
         "Connection": "keep-alive"
      }

    def get_all_problems(self, categorySlug: str, filters: dict, limit: int):
      data = {
        "query": get_problem_set_question_list_query(),
        "variables": {
          "categorySlug": categorySlug,
          "filters": filters,
          "limit": limit
        },
        "operationName": "problemsetQuestionList"
      }
      return requests.post(self.host, json=data, headers=self.headers)

    def get_submission_list(self, title_slug: str):
       data = {
          "query": get_submission_list_query(),
          "variables": {
            "lastKey": None,
			      "limit": 5,
			      "offset": 0,
			      "questionSlug": title_slug
          },
          "operationName": "submissionList"
       }
       return requests.post(self.host, json=data, headers=self.headers)

    def get_submission_details(self, submissionId: str):
       data = {
          "query": get_submission_details_query(),
          "variables": {
            "submissionId": submissionId
          },
          "operationName": "submissionDetails"
       }
       return requests.post(self.host, json=data, headers=self.headers)
