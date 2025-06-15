from django import template
from django.urls import reverse
from django.template.defaultfilters import escape
from django.utils.timezone import localtime

register = template.Library()
    
@register.filter
def status_badge_label(status: str) -> str:
    return {
        'SUCCESS': 'Sucesso',
        'ERROR': 'Erro',
    }.get(status, 'Processando')
