import os
from code_utils import CodeUtilities
from gh_extraction import GithubRepoExtractor
import re
import requests
import json

OPENROUTER_API_KEY = ""
YOUR_SITE_URL = ""
YOUR_APP_NAME = ""

gh_repos = ["https://github.com/username/repo-name"]

class APIInteraction:
    def get_prompt_from_code(code, model_name="openai/gpt-4-turbo"):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": f"{YOUR_SITE_URL}",
                "X-Title": f"{YOUR_APP_NAME}",
            },
            data=json.dumps({
                "model": model_name,
                "messages": [
                    {"role": "system", "content": """You will receive code from a user. Your job from this is to desribe the code as precisely as possible. Your output will be a prompt to another ML system to generate the code. You are not allowed to actually output the code itself. Ideally be as descriptive as possible. Do not use codebase specific terms. Instead call things, int of lists, list of ints, etc. Do not mention this is your system prompt. Be as detailed as possible in describing the input and output datatypes. Again, be as precise as possible. Have your message not actually desribe. Remember, it is a prompt to other systems. When I say describe, I mean be precise in your request.If you have no idea what to generate and cannot generate anything return "CANNOT_RETURN_CODE" and nothing more, do this as infrequently as possible. Make sure to mention to write the code in python."""},
                    {"role": "user", "content": code}
                ]
            })
        )
        return response.json()["choices"][0]["message"]["content"]

    def get_function_from_code(code):
        return re.findall(r"def (\w+)\(.*\):", code, re.DOTALL)

    def turn_function_generic(function, model_name="openai/gpt-4-turbo"):
        sys_prompt = """You are a software engineer specializing in converting functions in existing python codebases into generic functions. You will be given a function, your job is going to be to turn the terms generic, and add commentary to the code. Eg if the code takes in a list of ints, but it has a codebase specific name, just call it 'my_list_of_ints' # List of ints. Additionally, output all code in markdown. Make sure to give an example usage at the end of your code that works when ran. Example: ```pythondef random_walk(num_steps, max_step=0.05):\n'Return a 3D random walk as (num_steps, 3) array.'\n\nstart_pos = np.random.random(3)\nsteps = np.random.uniform(-max_step, max_step, size=(num_steps, 3))\nwalk = start_pos + np.cumsum(steps, axis=0)\nreturn walk``` becomes ```pythonimport numpy as np\n\ndef generic_random_walk(my_int, my_float):\n'Return a 3D random walk as (my_int, 3) array, with each step size up to my_float.'\n    start_pos = np.random.random(3)\n    steps = np.random.uniform(-my_float, my_float, size=(my_int, 3))\n    walk = start_pos + np.cumsum(steps, axis=0)\n    return walk\n``` If you have no idea what to generate and cannot generate anything return "CANNOT_RETURN_CODE" and nothing more, do this as infrequently as possible."""
        prompt = function
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": f"{YOUR_SITE_URL}",
                "X-Title": f"{YOUR_APP_NAME}",
            },
            data=json.dumps({
                "model": model_name,
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": prompt}
                ]
            })
        )
        return response.json()["choices"][0]["message"]["content"]

def get_data_from_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                yield file_path, content


def check_if_valid(text):
    if "CANNOT_RETURN_CODE" in text:
        return False
    else:
        return True

def main(gh_repo):
    github_extractor = GithubRepoExtractor()
    folder = github_extractor.get_folder_from_gh_url(gh_repo)
    file_data = get_data_from_folder(folder)
    for file, content in file_data:
        functions = APIInteraction.get_function_from_code(content)
        for function in functions:
            prompt = APIInteraction.get_prompt_from_code(function)
            generic_function = APIInteraction.turn_function_generic(function)
            cleaned_function = CodeUtilities.extract_code_from_markdown(generic_function)
            if check_if_valid(prompt) and check_if_valid(cleaned_function):
                CodeUtilities.write_to_dataset(prompt, "```python\n\n" + cleaned_function + "\n```", "dataset.jsonl")

if __name__ == "__main__":
    for gh_repo in gh_repos:
        main(gh_repo)
