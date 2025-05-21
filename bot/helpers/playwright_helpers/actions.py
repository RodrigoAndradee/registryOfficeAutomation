# Function to safe fill some input
def safe_fill(page, selector, value, field_name):
    try:
        page.fill(selector, value)
    except Exception as e:
        raise Exception(f"Erro ao preencher '{field_name}': {str(e)}")

# Function to safe click some button
def safe_click(page, selector, field_name):
    try:
        page.click(selector)
    except Exception as e:
        raise Exception(f"Erro ao clicar em '{field_name}': {str(e)}")
    
# Function to safe select some option
def safe_select_option(page, selector, label, field_name):
    try:
        page.select_option(selector, label=label)
    except Exception as e:
        raise Exception(f"Erro ao selecionar '{field_name}' com o valor '{label}': {str(e)}")

# Function to safe press some key
def safe_press(page, key, field_name):
    try:
        page.keyboard.press(key)
    except Exception as e:
        raise Exception(f"Erro ao pressionar '{key}' em '{field_name}': {str(e)}")
