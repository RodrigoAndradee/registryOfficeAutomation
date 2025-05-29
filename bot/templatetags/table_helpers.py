from django import template
from django.urls import reverse
from django.template.defaultfilters import escape
from django.utils.timezone import localtime

register = template.Library()

@register.filter
def get_status_badge_class(status: str) -> str:
    return {
        'SUCCESS': 'bg-success',
        'ERROR': 'bg-danger',
    }.get(status, 'bg-secondary')
    
@register.filter
def status_badge_label(status: str) -> str:
    return {
        'SUCCESS': 'Sucesso',
        'ERROR': 'Erro',
    }.get(status, 'Processando')

@register.simple_tag(takes_context=True)
def render_cell(context, value, column):
    path = column.get("path")
    content = getattr(value, path, "")
    
    # Cells with date type
    if hasattr(content, "strftime"):
        return localtime(content).strftime("%d/%m/%Y %H:%M:%S")
    
    if path == "status":
        return f'<span class="badge rounded-pill px-2 {get_status_badge_class(content)}">{status_badge_label(content)}</span>'
    
    if path == "action" and getattr(value, "can_retry", False):
        retry_url = reverse("retry_history", args=[getattr(value, "id")])
        csrf_token = context.get('csrf_token')  # O template engine deve passar isso
        return f'''
            <form action="{retry_url}" method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="{escape(csrf_token)}">
                <button type="submit" class="btn btn-sm btn-outline-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        class="bi bi-arrow-counterclockwise" viewBox="0 0 16 16">
                        <path fill-rule="evenodd"
                            d="M8 3a5 5 0 1 1-4.546 2.914.5.5 0 0 0-.908-.417A6 6 0 1 0 8 2z" />
                        <path
                            d="M8 4.466V.534a.25.25 0 0 0-.41-.192L5.23 2.308a.25.25 0 0 0 0 .384l2.36 1.966A.25.25 0 0 0 8 4.466" />
                    </svg>
                    Rodar Novamente
                </button>
            </form>
        '''
        
    return content
