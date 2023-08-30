# Implement basic keyword-based classification logic.
# Classify emails into categories such as "Important", "Promotions", "Personal", "AD" etc.


from .conf_imap import EmailType
# import api_openai
from .api_openai import chat_user_input, chat_sys_function, set_proxy
import time 

def email_classifier(the_email):
    messages = []
    chatlog = []
    date = time.strftime("%Y-%m-%d", time.localtime())
    chat_sys_function(f"Today is {date}" , messages, chatlog)
    chat_sys_function(\
"""
You are chatGPT, a LLM that can handle various text tasks. Noted that the user is a bioinformatician, while interested in AI and math. Your answer will be used to classify the email, please stick to the format. The user will input an email, you need to reply like:
SUMMARY: (a informative and direct summary in 60 words for the reader)
CATEGORY: (Spam / Notifications / Professional / Personal / Social / ... / not sure)
KEYWORDS: AI_tech:0.9, single_cell_seq:0.9, ... (2~6 keywords *with confidence score*)
PRIORITY: 0~6 (0: 'The final project dues tonight!'; 4: An invitation to a lecture in a week; 6: useless words)

""",messages,chatlog)
    return chat_user_input(str(the_email)[:2500], messages, chatlog, 0.1)

def email_classify(the_email, show_ans=False):
    assert type(the_email) == EmailType
    # TODO: phrase the result and update the email storage
    ans = email_classifier(the_email)
    if show_ans:
        print(ans)
    ans_lower = str(ans.lower())
    summary = ans[ans_lower.find("summary:")+9:ans_lower.find("category:")].strip()
    category = ans[ans_lower.find("category:")+9:ans_lower.find("keywords:")].strip()
    print(ans[ans_lower.find("priority:")+9:])
    priority = int(ans[ans_lower.find("priority:")+9:ans_lower.find("priority:")+11].strip())
    keywords = ans[ans_lower.find("keywords:")+9:ans_lower.find("priority:")].strip().split(",")
    try:
        keywords = [{keyword.split(":")[0]:keyword.split(":")[1]} for keyword in keywords]
    except:
        keywords = [{keyword:-1} for keyword in keywords]
    assert summary.count("\n") < 2
    assert category.count("\n") < 2
    assert keywords.count("\n") < 2
    setattr(the_email, "summary", summary)
    setattr(the_email, "category", category)
    setattr(the_email, "priority", priority)
    setattr(the_email, "keywords", keywords)
    return the_email

if __name__ == "__main__":
    set_proxy()
    from .conf_address import accounts
    from .email_fethcher import emails_load_json
    emails = []
    emails_load_json(accounts[0], emails)
    # print(type(emails[2]))
    print(email_classify(emails[4], True))