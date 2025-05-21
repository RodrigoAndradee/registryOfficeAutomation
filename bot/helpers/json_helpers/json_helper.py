import os

def validate_json_fields(data):
    if "automation_data" not in data:
        return False, "Campo 'automation_data' está ausente."

    if not isinstance(data["automation_data"], list):
        return False, "'automation_data' deve ser uma lista."

    for i, item in enumerate(data["automation_data"]):
        if not isinstance(item, dict):
            return False, f"Item {i} em 'automation_data' deve ser um objeto."

        for campo in ["code", "quantity", "type"]:
            if campo not in item:
                return False, f"Campo '{campo}' ausente no item {i}."

        if not isinstance(item["code"], str):
            return False, f"Campo 'code' no item {i} deve ser uma string."
        if not isinstance(item["quantity"], str):
            return False, f"Campo 'quantity' no item {i} deve ser um inteiro."
        if not isinstance(item["type"], str):
            return False, f"Campo 'type' no item {i} deve ser uma string."

    return True, ""

# This function breaks the json array in small arrays to match the workers amount    
def split_chunks(data):
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
