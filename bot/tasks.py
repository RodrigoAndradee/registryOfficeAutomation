import os
import json
from concurrent.futures import ThreadPoolExecutor
from celery import shared_task
from playwright.sync_api import sync_playwright
from django.utils import timezone

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
                        update_status(item_id, "ERROR")
        
            browser.close()
            
    except Exception as e:
        for item in data:
            item_id = item.get("item_id")

            if item_id:
                update_status(item_id, "ERROR")
        raise e

def update_status(item_id, status):
    # Updating the status on the database
    def task():
        from bot.models import AutomationHistory
        AutomationHistory.objects.filter(id=item_id).update(
            status=status, 
            finished_at=timezone.now()
        )
    
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(task)
        future.result()
