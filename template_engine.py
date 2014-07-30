import re

def apply_template(template, value_dict):
    for key in value_dict:
        template = re.sub("{{%s}}" % key, value_dict[key], template)
    return template
