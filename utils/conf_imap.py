 # IMAP ID information
from typing import Any


imap_id = {
    "name": "fezzymail",
    "version": "0.0.1",
    "vendor": "cmd",
    "support-email": "tellittofezzy@163.com"
}
pharser_keys = [
    "Subject",
    "From",
    "To",
    "Date",
    "Content-Type",
]
email_name_map = {
    "Subject": "subject",
    "From": "sender",
    "To": "receiver",
    "Date": "date",
    "Content-Type": "content_type",
}

class EmailType(object):
    def __init__(self, *args, **kwargs):
        self.id = None
        self.subject = None
        self.sender = None
        self.receiver = None
        self.date = None
        self.content_type = None
        self.body = ""
        self.summary = None
        self.category = []
        self.keywords = []
        self.priority = 0
        self.checked = False
        self.__dict__.update(kwargs)

    def __setattr__(self, __name: str, __value: Any) -> None:
        self.__dict__[__name] = __value

    def __str__(self) -> str:
        s = ""
        for key in self.__dict__:
            if key == "body":
                continue
            s += f"{key}: {self.__dict__[key]}\n"
        return s
    