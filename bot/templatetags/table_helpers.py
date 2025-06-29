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

@register.filter
def month_label(month: str) -> str:
    return {
        '2': 'Fevereiro',
        '3': 'Março',
        '4': 'Abril',
        '5': 'Maio',
        '6': 'Junho',
        '7': 'Julho',
        '8': 'Agosto',
        '9': 'Setembro',
        '10': 'Outubro',
        '11': 'Novembro',
        '12': 'Dezembro',
    }.get(month, 'Janeiro')

@register.filter
def get_range_until(start, end):
    return range(start, end + 1)
