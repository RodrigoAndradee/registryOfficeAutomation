import os
import json

from django.utils import timezone

from concurrent.futures import ThreadPoolExecutor
from celery import shared_task
from playwright.sync_api import sync_playwright, Page

from bot.helpers.playwright_helpers.actions import safe_click, safe_fill, safe_press, safe_select_option, safe_navigate, handle_dialog, check_no_alert

def fill_login_form(page: Page, fields) -> None:
    safe_fill(page, fields["input_inscription"], os.getenv("INPUT_INSCRIPTION"), "Inscrição")
    safe_fill(page, fields["input_cpf"], os.getenv("INPUT_CPF"), "CPF")
    safe_fill(page, fields["input_password"], os.getenv("INPUT_PASSWORD"), "Senha")

    safe_click(page, fields["login_button"], "Entrar")

def navigate_through_menu(page: Page, fields) -> None:
    page.hover(fields["registry_office"])
    safe_click(page, fields["declare"], "Declarar (Menu de navegação)")

def fill_form_content(page, fields, data):
    # Selecting Mayo just for testing.. Need to check if its really needed
    safe_select_option(page, fields["mounth"], "Maio", "Campo Mês")
    safe_fill(page, fields["code_act"], data["code"], "Código do Ato") 
    safe_press(page, 'Enter', "Código do Ato")
    page.wait_for_load_state('networkidle')
    check_no_alert(page, data["code"])

    if data["type"] != "Normal":
        safe_select_option(page, fields["type"], data["type"], 'Campo "Tipo"')

    safe_fill(page, fields["quantity"], str(data["quantity"]), "Quantidade")

    safe_click(page, fields["submit_form"], "Botão Confirmar")

@shared_task(bind=True)
def execute_form(self, data) -> None:
    json_file_path = os.path.join(os.path.dirname(__file__), 'static', 'data', 'form_fields.json')
    with open(json_file_path, 'r', encoding='utf-8') as file:
        form_fields = json.load(file)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.on("dialog", handle_dialog)
            safe_navigate(page, os.getenv("AUTOMATION_TARGET_URL"))

            fill_login_form(page, form_fields)
            navigate_through_menu(page, form_fields)
        
        except Exception as e:
            for item in data:
                item_id = item.get("item_id")

                if item_id:
                    update_status(item_id, "ERROR", str(e), True)
            raise e

        # Runs the automation on each position of the array
        for item in data:
            item_id = item.get("item_id")
            try: 
                fill_form_content(page, form_fields, item)

                if item_id:
                    update_status(item_id, "SUCCESS")
            except Exception as form_error:
                if item_id:
                    print("Mensagem:", str(form_error))
                    update_status(item_id, "ERROR", str(form_error))
    
        browser.close()

def update_status(item_id: int, status: str, error_message: str = None, can_retry: bool = False) -> None:
    # Updating the status on the database
    def task():
        from bot.models import AutomationHistory
        update_fields = {
            "status": status,
            "finished_at": timezone.now(),
            "can_retry": can_retry
        }

        if error_message is not None:
            update_fields["error_message"] = error_message

        AutomationHistory.objects.filter(id=item_id).update(**update_fields)
    
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(task)
        future.result()
