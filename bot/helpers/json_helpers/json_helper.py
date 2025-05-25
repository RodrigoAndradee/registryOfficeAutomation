import os

from typing import TypedDict, List, Tuple

class AutomationItem(TypedDict):
    code: int
    quantity: int
    type: str

class AutomationItemsList(TypedDict):
    List[AutomationItem]

class AutomationData(TypedDict):
    automation_data: AutomationItemsList

def validate_json_fields(data: AutomationData) -> Tuple[str, AutomationItemsList, AutomationItemsList]:
    valid_fields = []
    invalid_fields = []
    automation_data = data.get("automation_data")

    if "automation_data" not in data:
        return "Campo automation_data ausente no JSON!", valid_fields, invalid_fields

    if not isinstance(automation_data, list):
        return "Campo automation_data não é um array!", valid_fields, invalid_fields
    
    for i, item in enumerate(automation_data):
        if not isinstance(item, dict):
            invalid_fields.append({"message_error": f"Item {i} em 'automation_data' deve ser um objeto."})
            continue
            
        missing_fields = []
        for field in ["code", "quantity", "type"]:
            if field not in item:
                missing_fields.append(field)

        error_message = ", ".join(missing_fields)
        if len(error_message) > 0:
            invalid_fields.append({**item, "message_error": f"Campo(s) '{error_message}' ausente(s) no item {i}"})
            continue

        if not isinstance(item["code"], str):
            invalid_fields.append({**item, "message_error": f"Campo 'code' no item {i} deve ser uma string."})
            continue
        if not isinstance(item["quantity"], str):
            invalid_fields.append({**item, "message_error": f"Campo 'quantity' no item {i} deve ser uma string."})
            continue
        if not isinstance(item["type"], str):
            invalid_fields.append({**item, "message_error": f"Campo 'type' no item {i} deve ser uma string."})
            continue

        valid_fields.append(item)

    return "", valid_fields, invalid_fields

# This function breaks the json array in small arrays to match the workers amount    
def split_chunks(data: List[AutomationItem]) -> List[List[AutomationItem]]:
    workers_amount = int(os.getenv("WORKERS_AMOUNT", 1))

    if workers_amount <= 1:
        return [data]

    chunk_size = len(data) // workers_amount
    remainder = len(data) % workers_amount

    result = []
    start = 0

    for i in range(workers_amount):
        end = start + chunk_size + (1 if i < remainder else 0)
        result.append(data[start:end])
        start = end

    return result
