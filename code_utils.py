import re
import subprocess
import sys  
from io import StringIO

import json



class CodeUtilities:
    @staticmethod
    def extract_code_from_markdown(code):
        code_blocks = re.findall(r"```python\n(.*?)```", code, re.DOTALL)
        return '\n'.join(code_blocks)


    @staticmethod
    def install_packages(code):
        required_packages = set(re.findall(r'^import (\w+)|^from (\w+) import', code, re.MULTILINE))
        for package in required_packages:
            subprocess.run([sys.executable, "-m", "pip", "install", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    # This isn't functional yet. I'm working on testing it currently. 
    def test_code_from_api(code):
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = StringIO(), StringIO()
        try:
            CodeUtilities.install_packages(code)
            exec(code, {})
            return code
        except Exception as e:
            return f"Error occurred: {str(e)}"
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr

    @staticmethod
    def write_to_dataset(prompt, code, filename):
        data = {"prompt": prompt, "completion": code}
        with open(filename, "a") as file:
            file.write(json.dumps(data) + "\n")
