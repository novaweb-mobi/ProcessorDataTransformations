from typing import Set

from dictor import dictor

from utils import EventContent

HIDER = "x"
HIDE_LABEL = "hide"


def add_actions():
    return {
        "anonymize": {
            "operation": hide_content,
            "name": "Anonimizar dados",
            "data_fields": {
                "key": "fields",
                "label": "Campos a Anonimizar",
                "field_type": "object",
                "field_options": {
                    "property_key": {
                        "label": "Campo",
                        "field_type": "text",
                        "field_options": {
                            "format": "[^.]"
                        }
                    },
                    "property_value": {
                        "label": "Tipo de Campo",
                        "field_type": "select",
                        "field_options": {
                            "options": [
                                {
                                    "label": anonymizer_type["description"],
                                    "value": anonymizer_type_key
                                }
                                for anonymizer_type_key, anonymizer_type
                                in types.items()]
                        }
                    }
                }
            }
        }
    }


def replace_keeping_n_digits(digits_to_keep: int, replacer: str,
                             original: str, keep_start: bool):
    digits_to_replace = len(original) - digits_to_keep
    if keep_start:
        return original[:digits_to_keep] + (replacer * digits_to_replace)

    return (replacer * digits_to_replace) + original[-digits_to_keep:]


def change_phone(phone):
    phone = replace_keeping_n_digits(3, HIDER, str(phone), False)
    return phone


def change_general(value: str):
    thirty_percent = int(len(value) * 0.3)
    value = replace_keeping_n_digits(thirty_percent, HIDER,
                                     str(value), True)
    return value


def change_matricula(matricula):
    matricula = replace_keeping_n_digits(3, HIDER, str(matricula), True)
    return matricula


def change_cpf_cnpj(cpf: str):
    cpf = replace_keeping_n_digits(3, HIDER, str(cpf), True)
    return cpf


types = {
    "cpf": {
        "anonymizer": change_cpf_cnpj,
        "description": "CPF/CNPJ"
    },
    "telefone": {
        "anonymizer": change_phone,
        "description": "Telefone"
    },
    "matricula": {
        "anonymizer": change_matricula,
        "description": "Matrícula"
    },
    "default": {
        "anonymizer": change_general,
        "description": "Outros"
    }
}


def check_anonymize_type(field_type):
    return types.get(field_type, {}) \
        .get("anonymizer", change_general)


def hide_content(event_content: EventContent, data: dict):
    fields = data.get("fields", {})

    for field_name, field_type in fields.items():
        anonimize_operation = check_anonymize_type(field_type)

        event_content["event"]["content"]["content"][field_name] = \
            anonimize_operation(dictor(event_content,
                                       f"event.content.content.{field_name}",
                                       ""))

    return event_content
