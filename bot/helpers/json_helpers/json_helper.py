import os
from math import ceil
from typing import TypedDict, List, Tuple
from pydantic import BaseModel, Field, ValidationError

from django.utils import timezone

from bot.models import TypesOfTaxation


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
    error_message: str


class ValidItem(TypedDict):
    code: str
    quantity: int
    type: int
    mapped_type: int


AutomationItemsList = List[AutomationItem]
TaxationItemsList = List[TypesOfTaxation]

# Validate the code. If the last character is not valid adds the item to errors array
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
    return next((item for item in taxation_types if item.type == code), None)

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
                "error_message": f"Erro no item {index}: {err['msg']}",
                "status": "ERROR",
                "finished_at": timezone.now()
            })
        return valid_fields, invalid_fields

    for item in model.automation_data:
        
        # Checking if the code is correct
        code_base = item.code.split("-")[0]
        expected_code = calculate_check_digit_mod10(code_base)

        if item.code != expected_code:
            invalid_fields.append({
                "code": item.code,
                "quantity": item.quantity,
                "type": item.type,
                "error_message": f"Dígito verificador inválido. Esperado: <b>{expected_code}</b>",
                "status": "ERROR",
                "finished_at": timezone.now()
            })
            continue

        taxation_type = find_taxation_by_code(item.type, taxation_types)

        if taxation_type:
            # If there is some mapped type it means that we can run the automation
            if taxation_type.mapped_type is not None:
                valid_fields.append({
                    "code": item.code,
                    "quantity": item.quantity,
                    "type": item.type,
                    "mapped_type": taxation_type.mapped_type
                })
                continue
            
            invalid_fields.append({
                "code": item.code,
                "quantity": item.quantity,
                "type": item.type,
                "error_message": f"Tipo <b>{taxation_type.description}</b> não cadastrado!",
                "status": "ERROR",
                "finished_at": timezone.now()
            })
            continue
        
        invalid_fields.append({
            "code": item.code,
            "quantity": item.quantity,
            "type": item.type,
            "error_message": "Nenhum mapeamento encontrado, por favor contate o suporte!",
            "status": "ERROR",
            "finished_at": timezone.now()
        })

    return valid_fields, invalid_fields

# This function breaks the array into N(number of workers) smaller arrays to parallelize the execution.
def split_chunks(data: List[AutomationItem]) -> List[List[AutomationItem]]:
    workers = max(1, int(os.getenv("WORKERS_AMOUNT", 1)))
    chunk_size = ceil(len(data) / workers)
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
