from typing import Set
from utils import EventContent

HIDER = "x"
HIDE_LABEL = "hide"


def add_actions():
    return {
        "rename_fields": {
            "operation": hide_content,
            "name": "Criação de dados Anonimos"
        }
    }


def replacement(n: int, tag: str, base: str, place: bool):
    if not place:
        return tag*(len(base)-n) + base[-n:]
    return base[:n] + tag*(len(base)-n)


def change_phone(phone):
    phone = replacement(3, HIDER, str(phone), False)
    return phone


def change_general(value: str):
    value = replacement(int(len(value)*0.3), HIDER, value, True)
    return value


def change_matricula(matricula):
    matricula = replacement(3, HIDER, str(matricula), True)
    return matricula


def change_cpf_cnpj(cpf: str):
    cpf = replacement(3, HIDER, cpf, True)
    return cpf


def check_type(event, key, label):
    if event.get(label):
        if key.lower() == "cpf":
            event[label] = change_cpf_cnpj(event[label])
        else if key.lower() == "telefone":
            event[label] = change_phone(event[label])
        else if key.lower() == "matricula":
            event[label] = change_matricula(event[label])
        else:
            event[label] = change_general(event[label])
    return event


def hide_content(event_content: EventContent):
    events_to_hide = event_content.get("data", {}).get("content", {})

    if events_to_hide.get(HIDE_LABEL, {}) and events_to_hide:
        for label, type_ in events_to_hide[HIDE_LABEL].items():
            events_to_hide = check_type(events_to_hide, type_, label)
        event_content["data"]["content"] = events_to_hide
    return event_content
