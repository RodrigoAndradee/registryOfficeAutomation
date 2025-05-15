from django import template

register = template.Library()

@register.filter
def status_badge_class(status):
    return {
        'SUCCESS': 'bg-success',
        'ERROR': 'bg-danger',
        'PENDING': 'bg-warning',
    }.get(status, 'bg-secondary')

@register.filter
def status_badge_label(status):
    return {
        'SUCCESS': 'Sucesso',
        'ERROR': 'Erro',
        'PENDING': 'Processando'
    }.get(status, 'Processando')
