from django import template

register = template.Library()

@register.filter
def status_badge_class(status):
    return {
        'SUCCESS': 'bg-success',
        'ERROR': 'bg-danger',
    }.get(status, 'bg-secondary')

@register.filter
def status_badge_label(status):
    return {
        'SUCCESS': 'Sucesso',
        'ERROR': 'Erro',
        'PROCESSING': 'Processando'
    }.get(status, 'Processando')
