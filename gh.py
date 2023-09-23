import base64
import json
import requests

from logger import debug, info, set_logging

set_logging()

class GHApi:
  def __init__(self, access_token: str):
    self.access_token = access_token
    self.host = "https://api.github.com"
    self.repo = ""
    self.owner = ""
    self.headers = {
      "Authorization": f"Bearer {access_token}"
    }
    self.lang_map = {
      "python3": "py",
      "java": "java"
    }

  def get_user_info(self):
    return requests.get(f"{self.host}/user", headers={
        "Authorization": f"Bearer {self.access_token}"
    })

  def get_repo(self, owner: str, repo_name: str):
    return requests.get(f"{self.host}/repos/{owner}/{repo_name}", headers={
        "Authorization": f"Bearer {self.access_token}"
    })

  def create_repo(self, name: str):
    return requests.post(f"{self.host}/user/repos", headers={
        "Authorization": f"Bearer {self.access_token}"
    }, data=json.dumps({
      "name": name
    }))

  def is_file_exists(self, path: str):
    result = requests.get(path, headers=self.headers)
    return result

  def upsert(self, path: str, commit_message: str, content: str):
    file_exists = self.is_file_exists(path)
    base_64_content = str(base64.b64encode(content.encode("utf-8")), "utf-8")
    data = {
      "message": commit_message,
      "content": base_64_content,
    }
    if file_exists.status_code == 200:
      sha = file_exists.json()["sha"]
      data["sha"] = sha
    return requests.put(path, json=data, headers=self.headers)

  def upload_code(self, readme_content: str, title_slug: str, title: str, question_frontend_id: str, runtime: str, runtime_faster_than: float, memory: str, memory_less_than: float, code: str, lang_name: str):
    folder = f"{question_frontend_id}-{title_slug}"
    file = f"{question_frontend_id}. {title}.{self.lang_map.get(lang_name, lang_name)}"
    readme = "README.md"
    readme_path = f"{self.host}/repos/{self.owner}/{self.repo}/contents/{folder}/{readme}"
    upsert_readme_result = self.upsert(readme_path, "README", readme_content)
    debug("upsert readme result", upsert_readme_result.text)
    code_path = f"{self.host}/repos/{self.owner}/{self.repo}/contents/{folder}/{file}"
    upsert_code_result = self.upsert(code_path, f"Runtime: {runtime} {f'(faster than {runtime_faster_than}%)' if runtime_faster_than > 0 else ''}, Memory: {memory} {f'(less than {memory_less_than}%)' if memory_less_than > 0 else ''} - GitSync", code)
    debug("upsert code result", upsert_code_result.text)
    info(f"failed to upload question {question_frontend_id}") if upsert_code_result.status_code // 100 != 2 else info(f"successfully uploaded quesetion {question_frontend_id}")
