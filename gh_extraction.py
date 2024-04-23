
import requests
import re
import tempfile
import json
import os
import zipfile



class GithubRepoExtractor:
    @staticmethod
    def get_folder_from_gh_url(url):
        match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
        if not match:
            raise ValueError("Invalid GitHub URL")
        owner, repo = match.groups()

        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(api_url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch repository information: {response.status_code}")
        repo_info = json.loads(response.text)
        default_branch = repo_info["default_branch"]
        zip_url = f"https://github.com/{owner}/{repo}/archive/{default_branch}.zip"
        response = requests.get(zip_url)
        if response.status_code != 200:
            raise ValueError(f"Failed to download repository: {response.status_code}")

        return GithubRepoExtractor._unpack_zip(response.content, repo, default_branch)

    @staticmethod
    def _unpack_zip(content, repo, branch):
        temp_dir = tempfile.mkdtemp()
        temp_zip_path = os.path.join(temp_dir, f"{repo}-{branch}.zip")
        with open(temp_zip_path, "wb") as temp_file:
            temp_file.write(content)
        extract_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(temp_zip_path, "r") as zip_file:
            zip_file.extractall(extract_dir)
        return os.path.join(extract_dir, f"{repo}-{branch}")
