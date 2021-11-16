from utils import EventContent
from dictor import dictor


def add_actions():
    return {
        "capitalize": {
            "operation": capitalize,
            "name": "Capitalizar campo",
            "data_fields": [{
                "key": "field",
                "label": "Campo a Capitalizar",
                "field_type": "text",
                "field_options": {
                }
            }]
        }
    }


def capitalize(event_content: EventContent, data: dict):
    fields = data.get("field", {})
    path = fields.split(".")

    content = event_content["event"]["content"]["content"]
    for path_component in path[:-1]:
        content = content.get(path_component)

    content[path[-1]] = str(content[path[-1]]).upper()
    
    return event_content
