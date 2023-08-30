# Import IMAPClient and other necessary modules.
# Implement a function to connect to the email server and fetch emails.
# Parse email content (subject, sender, body) from fetched emails.

import json
import email
from email import policy
from email.parser import BytesParser
from .conf_imap import imap_id, pharser_keys, EmailType, email_name_map
from .conf_address import accounts
from .email_classifier import email_classify
from imapclient import IMAPClient
import sys
import os
from os import path as op

store_path = op.dirname(op.dirname(op.abspath(__file__)))
store_path = op.join(store_path, "storage", "emails")
print(store_path)

def emails_fetch(account):
    SERVER = account['imap']
    EMAIL_ADDRESS = account['email']
    EMAIL_PASSWORD = account['pwd']
    PORT = account['port']
    acc_folder = op.join(store_path, EMAIL_ADDRESS)
    if not op.exists(acc_folder):
        os.mkdir(acc_folder)
    # Connect to the Gmail server using IMAP.
    if SERVER == "imap.163.com":
        with IMAPClient(SERVER, port=PORT, use_uid=True) as server:
            server.id_(imap_id)
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.select_folder("INBOX")
            # Search for all email ids in the mailbox
            email_ids = server.search()
            # Retrieve email information for each email id
            for email_id in email_ids:
                filename = op.join(acc_folder, f"{email_id}.eml")
                if op.exists(filename):
                    continue
                msg_data = server.fetch([email_id], ["RFC822"])
                raw_email = msg_data[email_id][b"RFC822"]
                # Process the raw email content as needed
                with open(filename, "wb") as f:
                    f.write(raw_email)
                    f.close()
                # # print(raw_email.decode("utf-8"))
                # the_email = emails_phraser(raw_email)
                # with open(filename, "w") as f:
                #     json.dump(the_email.__dict__, f, indent=4)

def emails_phraser(raw_email):
    email_message = BytesParser(policy=policy.default).parsebytes(raw_email)
    the_email = EmailType()
    for key in pharser_keys:
        # print(f"{key}: {email_message[key]}")
        setattr(the_email, email_name_map[key], email_message.get(key))
    # print(email_message.get_payload(decode=True).decode("utf-8"))
    try:
        if email_message.is_multipart():
            for part in email_message.walk():
                try:
                    setattr(the_email, "body", the_email.body + part.get_body(preferencelist=("plain","html")).get_content())
                except:
                    pass
        setattr(the_email, "body", email_message.get_body(preferencelist=("plain","html")).get_content())
    except Exception as e:
        print(f"Error: email body pharsing failed.")
        raise e
    return the_email

def emails_cook_raw(account):
    acc_folder = op.join(store_path, account['email'])
    for filename in os.listdir(acc_folder):
        filepath = op.join(acc_folder, filename)
        if filename.endswith(".eml"):
            with open(filepath, "rb") as f:
                raw_email = f.read()
            the_email = emails_phraser(raw_email)
            print(the_email.subject)
            assert the_email.body != ""
            filepath = filepath.replace(".eml", ".json")
            if op.exists(filepath):
                continue
            setattr(the_email, "id", filename.replace(".eml", ""))
            # the_email = email_classify(the_email)
            with open(filepath, "w") as f:
                json.dump(the_email.__dict__, f, indent=4)
                f.close()
        # elif filename.endswith(".json"):
        #     with open(filepath, "r") as f:
        #         the_email = json.load(f)
            # print(the_email["subject"])

def emails_load_json(account, buffer):
    acc_folder = op.join(store_path, account['email'])
    for i, filename in enumerate(os.listdir(acc_folder)):
        filepath = op.join(acc_folder, filename)
        if filename.endswith(".json"):
            with open(filepath, "r") as f:
                j = json.load(f)
                f.close()
            the_email = EmailType(**j)
            if the_email.summary == None:
                try:
                    the_email = email_classify(the_email)
                    with open(filepath, "w") as f:
                        json.dump(the_email.__dict__, f, indent=4)
                        f.close()
                except Exception as e:
                    print(f"Error: {i} th email classification failed. {the_email.subject}")
                    raise e
            buffer.append(the_email)

def emails_set_id(account):
    # id is the filename
    acc_folder = op.join(store_path, account['email'])
    for i, filename in enumerate(os.listdir(acc_folder)):
        filepath = op.join(acc_folder, filename)
        if filename.endswith(".json"):
            with open(filepath, "r") as f:
                j = json.load(f)
                f.close()
            the_email = EmailType(**j)
            setattr(the_email, "id", filename.replace(".json", ""))
            with open(filepath, "w") as f:
                json.dump(the_email.__dict__, f, indent=4)
                f.close()

def emails_dump_json(account, buffer):
    acc_folder = op.join(store_path, account['email'])
    for i, email in enumerate(buffer):
        filepath = op.join(acc_folder, f"{email.id}.json")
        with open(filepath, "w") as f:
            json.dump(email.__dict__, f, indent=4)
    
if __name__ == "__main__":
    emails_fetch(accounts[0])
    emails_cook_raw(accounts[0])
    emails = []
    emails_load_json(accounts[0],emails)
    print(len(emails))