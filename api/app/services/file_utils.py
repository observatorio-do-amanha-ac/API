import re

def extract_range_from_name(name):
    match = re.match(r"\[(\d{4})-(\d{4})\]", name)
    return (match.group(1), match.group(2)) if match else (None, None)

def extract_suffix_from_name(name):
    return name.split('_')[-1].split('.')[0]
