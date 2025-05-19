import os
import json
from celery import shared_task
from bot.models import AutomationHistory
from playwright.sync_api import sync_playwright
from django.db import connection

def fill_login_form(page, fields):
    page.fill(fields["input_inscription"], os.getenv("INPUT_INSCRIPTION"))
    page.fill(fields["input_cpf"], os.getenv("INPUT_CPF"))
    page.fill(fields["input_password"], os.getenv("INPUT_PASSWORD"))
    page.click(fields["login_button"])

def navigate_through_menu(page, fields):
    page.hover(fields["registry_office"])
    page.click(fields["declare"])

def fill_form_content(page, fields, data):
    page.fill(fields["code_act"], data["code"])

@shared_task(bind=True)
def execute_form(self, data):
    history_instance = None
    
    json_file_path = os.path.join(os.path.dirname(__file__), 'static', 'data', 'form_fields.json')
    with open(json_file_path, 'r', encoding='utf-8') as file:
        form_fields = json.load(file)
    
    # Trying to login
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(os.getenv("ARAXA_URL"))

            fill_login_form(page, form_fields)
            navigate_through_menu(page, form_fields)

            # Runs the automation on each position of the array
            for item in data:
                try: 
                    history_instance = AutomationHistory.objects.create(
                        code = item["code"],
                        quantity = item["quantity"],
                        type = item["type"]
                    )
                    fill_form_content(page, form_fields, item)

                    # Updating the status on the database
                    AutomationHistory.objects.filter(id=history_instance.history_id).update(status="SUCCESS")
                except Exception as form_error:
                    # Updating the status on the database
                    AutomationHistory.objects.filter(id=history_instance.history_id).update(status="ERROR")
        
            connection.close()
            browser.close()
            
    except Exception as e:
        raise e
