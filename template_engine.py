import re

def apply_template(template, value_dict):
    for key in value_dict:
        template = re.sub("{{%s}}" % key, value_dict[key], template.decode("utf-8").encode("ascii", "replace"))
    return template
