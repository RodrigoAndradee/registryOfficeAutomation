from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

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
def safe_navigate(page: Page, araxa_url: str) -> None:
    try:
        page.goto(araxa_url)
    except Exception as e:
        raise Exception("Erro! O Site pode estar indisponível!")

# Function to close the dialog
def handle_dialog(dialog):
    dialog.accept()

# Function to check if there is no alert 
def check_no_alert(page: Page, code_act: int) -> None:
    try:
        page.wait_for_event("dialog", timeout=5000)
        raise Exception(f"Código do Ato ({code_act}) inválido!")
    except PlaywrightTimeoutError:
        return None
