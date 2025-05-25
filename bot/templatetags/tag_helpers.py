from django import template

register = template.Library()

@register.filter
def status_badge_class(status: str) -> str:
    return {
        'SUCCESS': 'bg-success',
        'ERROR': 'bg-danger',
    }.get(status, 'bg-secondary')

@register.filter
def status_badge_label(status: str) -> str:
    return {
        'SUCCESS': 'Sucesso',
        'ERROR': 'Erro',
        'PROCESSING': 'Processando'
    }.get(status, 'Processando')
