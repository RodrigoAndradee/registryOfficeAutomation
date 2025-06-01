from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from typing import Dict

# Function to safe fill some input
def safe_fill(page: Page, selector: str, value: str, field_name: str) -> None:
    try:
        page.fill(selector, value)
    except Exception as e:
        raise Exception(f"Erro ao preencher '{field_name}'")

# Function to safe click some button
def safe_click(page: Page, selector: str, field_name: str) -> None:
    try:
        page.click(selector)
    except Exception as e:
        raise Exception(f"Erro ao clicar em '{field_name}'")
    
# Function to safe select some option
def safe_select_option(page: Page, selector: str, label: str, field_name: str) -> None:
    try:
        page.select_option(selector, label=label)
    except Exception as e:
        raise Exception(f"Erro ao selecionar '{field_name}' com o valor '{label}'")

# Function to safe press some key
def safe_press(page: Page, key: str, field_name: str) -> None:
    try:
        page.keyboard.press(key)
    except Exception as e:
        raise Exception(f"Erro ao pressionar '{key}' em '{field_name}'")

# Function to safe check if the site is open
def safe_navigate(page: Page, site_url: str) -> None:
    try:
        page.goto(site_url)
    except Exception as e:
        raise Exception("Erro! O Site pode estar indisponível!")

def listen_for_all_dialogs(page: Page, error_store: Dict[str, str]):
    def handle_dialog(dialog):
        error_store["message"] = dialog.message
        dialog.accept()

    page.on("dialog", handle_dialog)

# Function to close the dialog
def handle_dialog(dialog) -> str:
    dialog.accept()

# Function to check if there is no alert 
def check_no_alert(page: Page, code_act: int) -> None:
    try:
        page.wait_for_event("dialog", timeout=5000)
        raise Exception(f"Código do Ato ({code_act}) inválido!")
    except PlaywrightTimeoutError:
        return None
