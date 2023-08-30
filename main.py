# Import necessary modules from the ui and email_utils packages.
# Set up the main application loop.
# Implement the logic to fetch emails, generate summaries, classify, and display notifications.

import time
from ui.sfx import sound_mail, sound_guard
from ui.app import notification
from utils.conf_address import accounts
from utils.email_fethcher import emails_fetch, emails_load_json, emails_cook_raw, emails_dump_json, emails_set_id
from utils.email_classifier import email_classifier
from utils.api_openai import set_proxy

def check_emails():
    for account in accounts:
        emails = []
        emails_fetch(account)
        emails_cook_raw(account)
        emails_load_json(account, emails)
        for email in emails:
            if email.checked == False:
                notification("New Email", email)
                sound_mail()
                sound_guard()
                setattr(email, "checked", True)
        emails_dump_json(account, emails)

def set_checked_all():
    for account in accounts:
        emails = []
        emails_load_json(account, emails)
        for email in emails:
            setattr(email, "checked", True)
        emails_dump_json(account, emails)

if __name__ == "__main__":
    # set_proxy()
    # check_emails()
    # emails_set_id(accounts[0])
    # set_checked_all()
    while True:
        check_emails()
        time.sleep(60)