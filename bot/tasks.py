import os
import json

from concurrent.futures import ThreadPoolExecutor
from celery import shared_task
from playwright.sync_api import sync_playwright
from django.utils import timezone

from bot.helpers.playwright_helpers.actions import safe_click, safe_fill, safe_press, safe_select_option


def fill_login_form(page, fields):
    safe_fill(page, fields["input_inscription"], os.getenv("INPUT_INSCRIPTION"), "Inscrição")
    safe_fill(page, fields["input_cpf"], os.getenv("INPUT_CPF"), "CPF")
    safe_fill(page, fields["input_password"], os.getenv("INPUT_PASSWORD"), "Senha")

    safe_click(page, fields["login_button"], "Entrar")

def navigate_through_menu(page, fields):
    page.hover(fields["registry_office"])
    safe_click(page, fields["declare"], "Declarar (Menu de navegação)")

def fill_form_content(page, fields, data):
    safe_fill(page, fields["code_act"], data["code"], "Código do Ato")

    safe_press(page, 'Enter', "Código do Ato")
    page.wait_for_load_state('networkidle')

    if data["type"] != "Normal":
        safe_select_option(page, fields["type"], data["type"], "Tipo de Ato")

    safe_fill(page, fields["quantity"], str(data["quantity"]), "Quantidade")

    # TODO: Click on confirm button
    # safe_click(page, fields["confirm_button"], "Botão Confirmar")

@shared_task(bind=True)
def execute_form(self, data):
    json_file_path = os.path.join(os.path.dirname(__file__), 'static', 'data', 'form_fields.json')
    with open(json_file_path, 'r', encoding='utf-8') as file:
        form_fields = json.load(file)
    
    # Trying to login
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(os.getenv("ARAXA_URL"))

            fill_login_form(page, form_fields)
            navigate_through_menu(page, form_fields)

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
            
    except Exception as e:
        for item in data:
            item_id = item.get("item_id")

            if item_id:
                print("Mensagem:", str(e))
                update_status(item_id, "ERROR", str(e))
        raise e

def update_status(item_id, status, error_message = None):
    # Updating the status on the database
    def task():
        from bot.models import AutomationHistory
        update_fields = {
            "status": status,
            "finished_at": timezone.now()
        }

        if error_message is not None:
            update_fields["error_message"] = error_message

        AutomationHistory.objects.filter(id=item_id).update(**update_fields)
    
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(task)
        future.result()
