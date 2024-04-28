  import subprocess
from code_utils import CodeUtilities
from api_interaction import APIInteraction
import os


model_name='anthropic/claude-3-haiku'

def approximate_code(code, language="python"):
    executed_code = code
    if code.strip() == "":
        example_request = f"Add an example input and output for the following {language} code:\n{code}. Make sure that the output of the script is printed at the end if possible. If the output will be very long and hard to parse print the shape len and other critical information in the program. Output code in markdown."

        response = APIInteraction.call_openrouter(code, example_request, model_name)
        code_with_example = CodeUtilities.extract_code_from_markdown(response.json()["choices"][0]["message"]["content"])
        executed_code = code_with_example
        if language == "python":
            output = subprocess.check_output(["python", "-c", code_with_example], universal_newlines=True)
        elif language in ["js", "javascript", "node"]:
            output = subprocess.check_output(["node", "-e", code_with_example], universal_newlines=True)
        elif language in ["java"]:
            filename_with_example = f"MainWithExample_{CodeUtilities.generate_random_string(5)}.java"
            with open(filename_with_example, "w") as f:
                f.write(code_with_example)
            subprocess.run(["javac", filename_with_example], check=True)
            output = subprocess.check_output(["java", filename_with_example[:-5]], universal_newlines=True)
            os.remove(filename_with_example)
        elif language in ["c++", "cpp"]:
            filename_with_example = f"main_with_example_{CodeUtilities.generate_random_string(5)}.cpp"
            with open(filename_with_example, "w") as f:  
                f.write(code_with_example)
            subprocess.run(["g++", "-o", filename_with_example[:-4], filename_with_example], check=True)
            output = subprocess.check_output([f"./{filename_with_example[:-4]}"], universal_newlines=True)
            os.remove(filename_with_example)
            os.remove(filename_with_example[:-4])
        else:
            raise ValueError(f"Unsupported language: {language}")
    else:
        if language == "python":
            try:
                output = subprocess.check_output(["python", "-c", code], universal_newlines=True)
            except subprocess.CalledProcessError:
                example_request = f"Add an example input and output for the following {language} code:\n{code}. Make sure that the output of the script is printed at the end if possible. If the output will be very long and hard to parse print the shape len and other critical information in the program. Output code in markdown."

                response = APIInteraction.call_openrouter(code, example_request, model_name)
                code_with_example = CodeUtilities.extract_code_from_markdown(response.json()["choices"][0]["message"]["content"])
                executed_code = code_with_example
                output = subprocess.check_output(["python", "-c", code_with_example], universal_newlines=True)
        elif language in ["js", "javascript", "node"]:
            try:
                output = subprocess.check_output(["node", "-e", code], universal_newlines=True)
            except subprocess.CalledProcessError:
                example_request = f"Add an example input and output for the following {language} code:\n{code}. Make sure that the output of the script is printed at the end if possible. If the output will be very long and hard to parse print the shape len and other critical information in the program. Output code in markdown."

                response = APIInteraction.call_openrouter(code, example_request, model_name)
                code_with_example = CodeUtilities.extract_code_from_markdown(response.json()["choices"][0]["message"]["content"])
                executed_code = code_with_example
                output = subprocess.check_output(["node", "-e", code_with_example], universal_newlines=True)
        elif language in ["java"]:
            filename = f"Main_{CodeUtilities.generate_random_string(5)}.java"
            with open(filename, "w") as f:
                f.write(code)
            try:
                subprocess.run(["javac", filename], check=True)
                output = subprocess.check_output(["java", filename[:-5]], universal_newlines=True)
            except subprocess.CalledProcessError:
                example_request = f"Add an example input and output for the following {language} code:\n{code}. Make sure that the output of the script is printed at the end if possible. If the output will be very long and hard to parse print the shape len and other critical information in the program. Output code in markdown."

                response = APIInteraction.call_openrouter(code, example_request, model_name)
                code_with_example = CodeUtilities.extract_code_from_markdown(response.json()["choices"][0]["message"]["content"])
                executed_code = code_with_example
                filename_with_example = f"MainWithExample_{CodeUtilities.generate_random_string(5)}.java"
                with open(filename_with_example, "w") as f:
                    f.write(code_with_example)
                subprocess.run(["javac", filename_with_example], check=True)
                output = subprocess.check_output(["java", filename_with_example[:-5]], universal_newlines=True)
                os.remove(filename_with_example)
            os.remove(filename)
        elif language in ["c++", "cpp"]:
            filename = f"main_{CodeUtilities.generate_random_string(5)}.cpp"
            with open(filename, "w") as f:
                f.write(code)
            try:
                subprocess.run(["g++", "-o", filename[:-4], filename], check=True)
                output = subprocess.check_output([f"./{filename[:-4]}"], universal_newlines=True)
            except subprocess.CalledProcessError:
                example_request = f"Add an example input and output for the following {language} code:\n{code}. Make sure that the output of the script is printed at the end if possible. If the output will be very long and hard to parse print the shape len and other critical information in the program. Output code in markdown."

                response = APIInteraction.call_openrouter(code, example_request, model_name)
                code_with_example = CodeUtilities.extract_code_from_markdown(response.json()["choices"][0]["message"]["content"])
                executed_code = code_with_example
                filename_with_example = f"main_with_example_{CodeUtilities.generate_random_string(5)}.cpp"
                with open(filename_with_example, "w") as f:  
                    f.write(code_with_example)
                subprocess.run(["g++", "-o", filename_with_example[:-4], filename_with_example], check=True)
                output = subprocess.check_output([f"./{filename_with_example[:-4]}"], universal_newlines=True)
                os.remove(filename_with_example)
                os.remove(filename_with_example[:-4])
            os.remove(filename) 
            os.remove(filename[:-4])
        else:
            raise ValueError(f"Unsupported language: {language}")
    
    return executed_code, output



code, output = approximate_code("X=55\n\ni = X*55\n\nprint(i)", "python");
print("Code:")
print(code)
print("Output:")
print(output)

