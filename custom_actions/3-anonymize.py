from typing import Set
import string
import random

from dictor import dictor

from utils import EventContent

HIDER = "x"
HIDE_LABEL = "hide"


def add_actions():
    return {
        "anom": {
            "operation": anom_content,
            "name": "Anonimizar dados",
            "data_fields": [{
                "key": "field",
                "label": "Campo a Anonimizar",
                "field_type": "text",
                "field_options": {
                    "format": "[^.]"                    
                }
            }]
        }
    }


def anom_content(event_content: EventContent, data: dict):
    field = data.get("field", {})

    field_content = dictor(f"event.content.content.{field}")

    if not isinstance(field_content, str):
        return event_content

    for i,char in enumerate(field_content):
        if char in string.digits:
            field_content[i] = random.choice(string.digits)
        elif char in string.whitespace:
            field_content[i] = char
        else:
            field_content[i] = random.choice(string.ascii_letters)

    path = field.split(".")

    content = event_content["event"]["content"]["content"]
    for path_component in path[:-1]:
        content = content.get(path_component)

    content[path[-1]] = field_content

    return event_content
