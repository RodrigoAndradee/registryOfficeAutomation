from dotenv import load_dotenv
import os
from celery import shared_task
from playwright.sync_api import sync_playwright
import json

load_dotenv()

def fill_login_form(page, fields):
    # TODO: Move this sensitive data to venv
    page.fill(fields["input_inscription"], os.getenv("INPUT_INSCRIPTION"))
    page.fill(fields["input_cpf"], os.getenv("INPUT_CPF"))
    page.fill(fields["input_password"], os.getenv("INPUT_PASSWORD"))

    page.click(fields["login_button"])

    # Wait login action
    page.wait_for_timeout(100)

def navigate_through_menu(page, fields):
    page.hover(fields["registry_office"])
    page.click(fields["declare"])
    
@shared_task
def execute_form():
    json_file_path = os.path.join(os.path.dirname(__file__), 'static', 'data', 'form_fields.json')

    with open(json_file_path, 'r', encoding='utf-8') as file:
        login_fields = json.load(file)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://nfe.araxa.mg.gov.br/default.aspx")

        fill_login_form(page, login_fields)
        navigate_through_menu(page, login_fields)

        # TODO: Remove the following line. It's used just to test
        page.wait_for_timeout(5000)

        browser.close()


