# Implement basic keyword-based classification logic.
# Classify emails into categories such as "Important", "Promotions", "Personal", "AD" etc.

from conf_address import accounts
from email_fethcher import emails_load_json
# import api_openai
from api_openai import chat_user_input, chat_sys_function, set_proxy

def email_classifier(the_email):
    messages = []
    chatlog = []
    chat_sys_function(\
"""
You are chatGPT, a LLM that can handle various text tasks. The user will input an email, you need to reply like:
SUMMARY: (a informative and direct summary in 60 words for the reader)
CATEGORY: (Spam / Notifications / Issue / Professional / Personal / Social / ... / not sure)
KEYWORDS: AI_tech:0.9, ... (2~6 keywords, with confidence score)
PRIORITY: (0: deadly if not handled now; 6: useless words)
""",messages,chatlog)
    ans = chat_user_input(str(the_email), messages, chatlog, 0)
    return ans

set_proxy()
emails = []
emails_load_json(accounts[0], emails)
print(email_classifier(emails[0]))