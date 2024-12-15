import re


def extract_runtime(runtime_str):
    match = re.search(r"(\d+)", runtime_str)
    return int(match.group(1)) if match else None
