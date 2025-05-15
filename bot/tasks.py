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

def fill_form_content(page, fields):
    page.fill(fields["code_act"], "	4127-7")

@shared_task(bind=True)
def execute_form(self, history_id):
    
    json_file_path = os.path.join(os.path.dirname(__file__), 'static', 'data', 'form_fields.json')
    with open(json_file_path, 'r', encoding='utf-8') as file:
        form_fields = json.load(file)
        # print("JSON CONTENT", json.dumps(login_fields, indent=4, ensure_ascii=False))

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(os.getenv("ARAXA_URL"))

            fill_login_form(page, form_fields)
            navigate_through_menu(page, form_fields)
            fill_form_content(page, form_fields)
            browser.close()

        AutomationHistory.objects.filter(id=history_id).update(status="SUCCESS")
        connection.close()

    except Exception as e:
        AutomationHistory.objects.filter(id=history_id).update(status="ERROR")
        connection.close()
        raise e
