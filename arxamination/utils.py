import re
import os


def make_bold(text: str):
    return f"\033[1m{text}\033[0m"


def is_arxiv_id(s: str) -> bool:
    return bool(re.match(r"^\d{4}\.\d{5}$", s))


def is_url(s: str) -> bool:
    return s.startswith(("http://", "https://", "www."))


def is_file(s: str) -> bool:
    return s.endswith(".pdf")


def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)
