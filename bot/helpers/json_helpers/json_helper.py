import os
from math import ceil
from bot.models import TypesOfTaxation
from pydantic import BaseModel, Field, ValidationError
from typing import TypedDict, List, Tuple


class AutomationItem(BaseModel):
    code: str = Field(..., pattern=r'^\d{4}-\d$')
    quantity: int
    type: int


class AutomationItemsModel(BaseModel):
    automation_data: List[AutomationItem]

class InvalidItem(TypedDict):
    code: str
    quantity: int
    type: int
    message_error: str


class ValidItem(TypedDict):
    code: str
    quantity: int
    type: int


AutomationItemsList = List[AutomationItem]
TaxationItemsList = List[TypesOfTaxation]


def calculate_check_digit_mod10(code: str) -> str:
    weights = [2, 1]
    total = 0

    for i, digit in enumerate(reversed(code)):
        n = int(digit)
        weight = weights[i % 2]
        product = n * weight
        if product >= 10:
            product -= 9
        total += product

    remainder = total % 10
    check_digit = (10 - remainder) if remainder != 0 else 0
    return f"{code}-{check_digit}"


def find_taxation_by_code(code: int, taxation_types: TaxationItemsList):
    return next((item for item in taxation_types if item.code == code), None)

def validate_json_fields(raw_data: dict, taxation_types: List[TypesOfTaxation]) -> Tuple[List[ValidItem], List[InvalidItem]]:
    valid_fields: List[ValidItem] = []
    invalid_fields: List[InvalidItem] = []
    
    automation_data = raw_data.get("automation_data")
    
    if "automation_data" not in raw_data:
        raise Exception("Campo automation_data ausente no JSON!")
        
    if not isinstance(automation_data, list):
        raise Exception("Campo automation_data não é um array!")
    
    try:
        model = AutomationItemsModel(**raw_data)
    except ValidationError as e:
        print("Error", e)
        for err in e.errors():
            index = err['loc'][1] if len(err['loc']) > 1 else "?"
            invalid_fields.append({
                "code": "",
                "quantity": 0,
                "type": 0,
                "message_error": f"Erro no item {index}: {err['msg']}"
            })
        return valid_fields, invalid_fields

    for item in model.automation_data:
        # Validação do dígito verificador
        code_base = item.code.split("-")[0]
        expected_code = calculate_check_digit_mod10(code_base)

        if item.code != expected_code:
            invalid_fields.append({
                "code": item.code,
                "quantity": item.quantity,
                "type": item.type,
                "message_error": f"Dígito verificador inválido. Esperado: {expected_code}"
            })
            continue

        taxation_type = find_taxation_by_code(item.type, taxation_types)

        if taxation_type:
            if taxation_type.should_run_automation:
                valid_fields.append({
                    "code": item.code,
                    "quantity": item.quantity,
                    "type": taxation_type.mapped_value
                })
            else:
                invalid_fields.append({
                    "code": item.code,
                    "quantity": item.quantity,
                    "type": item.type,
                    "message_error": f"Erro para executar: {taxation_type.description}"
                })
        else:
            invalid_fields.append({
                "code": item.code,
                "quantity": item.quantity,
                "type": item.type,
                "message_error": "Nenhum mapeamento encontrado, por favor contate o suporte!"
            })

    return valid_fields, invalid_fields


def split_chunks(data: List[AutomationItem]) -> List[List[AutomationItem]]:
    workers = max(1, int(os.getenv("WORKERS_AMOUNT", 1)))
    chunk_size = ceil(len(data) / workers)
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
