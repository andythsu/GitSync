import json
from logging import debug
import os
from time import sleep

import requests

from gh import GHApi
from lc import LCApi
from logger import debug, info, set_logging

set_logging()

GH_API_HOST = "https://api.github.com"

def create_new_repo(gh_api: GHApi, repo_name: str):
    create_repo = gh_api.create_repo(repo_name)
    if create_repo.status_code // 100 == 4:
        debug("create_repo", create_repo.text)
        info("failed to create repo")
        return False
    else:
        info(f"successfully created repo {repo_name}")
        return True


def main():
    access_token = "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"

    gh_api = GHApi(access_token=access_token)

    user_info_json = gh_api.get_user_info().json()
    owner = user_info_json["login"]
    debug("owner", owner)
    gh_api.owner = owner
    # get repo name
    repo_name = input("Enter the repo name you want to sync to: ")

    get_repo = gh_api.get_repo(owner, repo_name)

    if get_repo.status_code == 404:
        ans = input(f"The repo {repo_name} doesn't exist. Create a new one? [y/n] ")
        if ans.capitalize() == 'Y':
            if not create_new_repo(gh_api, repo_name):
                exit(1)
        else:
            info("exiting...")
            exit(0)
    elif (get_repo.status_code // 100) == 4 or (get_repo.status_code // 100 == 5):
        info("unknown error occurred")
        debug("get_repo", get_repo.text)
        exit(1)

    gh_api.repo = repo_name

    # query leetcode problems
    lc_api = LCApi()
    info("retrieving problems from Leetcode")
    problems = lc_api.get_all_problems("", {}, 1)
    total_questions = int(problems.json()["data"]["problemsetQuestionList"]["total"])
    problems = lc_api.get_all_problems("", {}, total_questions)
    if problems.status_code != 200:
        debug("problems", problems.text)
        info("failed to retrieve problems")
        exit(1)
    info("retrieved all problems")
    questions = problems.json()["data"]["problemsetQuestionList"]["questions"]
    debug("questions", questions)
    for i in range(0, len(questions)):
        q = questions[i]
        info(f"syncing question {i}")
        title_slug = q["titleSlug"]
        title = q["title"]
        content = q["content"]
        question_frontend_id = q["questionFrontendId"]
        submissions = lc_api.get_submission_list(title_slug).json()["data"]["questionSubmissionList"]["submissions"]

        if len(submissions) == 0:
            info(f"no submissions found for question {i}. Skipping.")
            continue

        first_submission = submissions[0]
        debug("first_submission", first_submission)
        submission_details = lc_api.get_submission_details(first_submission["id"]).json()["data"]["submissionDetails"]
        debug("submission_details", submission_details)
        runtime = submission_details["runtimeDisplay"]
        runtime_faster_than = -1 if "runtimePercentile" not in submission_details or submission_details["runtimePercentile"] is None else round(submission_details["runtimePercentile"], 2)
        memory = submission_details["memoryDisplay"]
        memory_less_than = -1 if "memoryPercentile" not in submission_details or submission_details["memoryPercentile"] is None else round(submission_details["memoryPercentile"], 2)
        code = submission_details["code"]
        lang_name = submission_details["lang"]["name"]
        gh_api.upload_code(content, title_slug, title, question_frontend_id, runtime, runtime_faster_than, memory, memory_less_than, code, lang_name)
    info("done")

if __name__ == "__main__":
    main()
