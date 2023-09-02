# generate config files
import os

# Path: utils/conf_address.py
open("utils/conf_address.py", "w").write("""accounts = [
    {
        "email": ""
        "pwd": ""
        "imap": "imap.163.com",
        "port": 993,
    },
]""")
print("utils/conf_address.py generated.")

# Path: utils/conf_openai.py
open("utils/conf_openai.py", "w").write(
"""testing = False
temperature = 0
gpt4 = False
key = ""
proxies = {
    "http": "http://localhost:7890",
    "https": "http://localhost:7890",
}
import os
os.environ["OPENAI_API_KEY"] = key
sys_default = "You are ChatGPT, a large language model trained by OpenAI, based on the GPT architecture."
""")
print("utils/conf_openai.py generated.")


print("Please fill in the email address and password in utils/conf_address.py.")
print("Please fill in the OpenAI API key in utils/conf_openai.py.")