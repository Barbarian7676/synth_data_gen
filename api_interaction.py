import requests
import json
import re



OPENROUTER_API_KEY = ""
YOUR_SITE_URL = ""
YOUR_APP_NAME = ""


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
                    {"role": "user", "content": function}
                ]
            })
        )
        return response.json()["choices"][0]["message"]["content"]


    def convert_page_to_qa(website, model_name="openai/gpt-4-turbo"):
        system_prompt = "You are an expert at summarization and generating Q and A pairs based on a given website. You are an expert writer. The user will give you a set of unstructured data, usually a wikipedia or other encyclopedia page. Your job is to develop Q and A pairs based on the information within. Take all the relevant facts, list them, then output 'Question: YOUR_QUESTION_HERE, Answer: Answer here' Of course replace YOUR_QUESTION_HERE and Answer Here with the actual information for the QA pairs."
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
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": website}
                ]
            })
        )
        return response.json()["choices"][0]["message"]["content"]


    def generate_top_facts(data, model_name="openai/gpt-4-turbo"):
        system_prompt = "You will be given a wikipedia or other encyclopedia article. Your job is going to be to list the top 10 most interesting and relevant facts in the article. Please format your responses as follows: 1:\ntop_fact_1\n\n2:\ntop_fact_2....etc etc \n10:top_fact_10\n. "
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
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": data}
                ]
            })
        )
        return response.json()["choices"][0]["message"]["content"]

    def generate_summaries(data, model_name="openai/gpt-4-turbo"):
        system_prompt="you are an expert writer. You will be given a wikipedia, encyclopedia, or other news article. Please summarize the article."
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
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": data}
                ]
            })
        )
        return response.json()["choices"][0]["message"]["content"]
