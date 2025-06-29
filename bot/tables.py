from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse

import django_tables2 as tables

from bot.models import AutomationHistory

def common_render_status(self, record):
    def get_status_badge_class(status: str) -> str:
        return {
            'SUCCESS': 'bg-success',
            'ERROR': 'bg-danger',
        }.get(status, 'bg-secondary')
            
    def status_badge_label(status: str) -> str:
        return {
            'SUCCESS': 'Sucesso',
            'ERROR': 'Erro',
        }.get(status, 'Processando')
    
    def get_icon(status: str) -> str:
        return {
            'SUCCESS': format_html('<i class="bi bi-check-circle fs-6"></i>'),
            'ERROR': format_html('<i class="bi bi-exclamation-circle fs-6"></i>')
        }.get(status, format_html('<div class="spinner-border text-light spinner-border-sm" role="status"></div>'))
    
    status = record.status
    badge_class = get_status_badge_class(status)
    label = status_badge_label(status)
    icon = get_icon(status)

    return format_html(
        '<span class="badge rounded-pill px-2 d-flex align-items-center gap-1 {}" style="width: fit-content;">{}{}</span>',
        badge_class,
        icon,
        label
    )

class AutomationHistoryTable(tables.Table):
    id = tables.Column(attrs={"td": {"style": "width: 70px;"}})
    code = tables.Column(verbose_name="Código", attrs={"td": {"style": "width: 80px;"}})
    quantity = tables.Column(verbose_name="Quantidade", attrs={"td": {"style": "width: 90px;"}})
    type = tables.Column(verbose_name="Tipo", attrs={"td": {"style": "width: 55px;"}})
    created_at = tables.DateTimeColumn(format="d/m/Y H:i", verbose_name="Criado em", attrs={"td": {"style": "width: 150px;"}})
    finished_at = tables.DateTimeColumn(format="d/m/Y H:i", verbose_name="Finalizado em", default="", attrs={"td": {"style": "width: 150px;"}})
    error_message = tables.Column(verbose_name="Mensagem de Erro", default="")
    status = tables.Column(verbose_name="Status", attrs={"td": {"style": "width: 130px; padding: 8px 12px; "}})
    
    # action = tables.TemplateColumn(template_name="bot/automation_history_actions_column.html", verbose_name="Ações")

    def render_status(self, record):
        return common_render_status(self, record)
        
    # Used to bold the error message
    def render_error_message(self, value):
        if not value:
            return ""
        return mark_safe(value)

    class Meta:
        model = AutomationHistory
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            "id",
            "code", 
            "quantity", 
            "type", 
            "created_at", 
            "finished_at",
            "error_message",
            "status",
        )
        
class HistoryDetailsTable(tables.Table):
    code = tables.Column(verbose_name="Código", attrs={"td": {"style": "width: 80px;"}})
    quantity = tables.Column(verbose_name="Quantidade", attrs={"td": {"style": "width: 90px;"}})
    type = tables.Column(verbose_name="Tipo", attrs={"td": {"style": "width: 55px;"}})
    error_message = tables.Column(verbose_name="Mensagem de Erro")

    # Used to bold the error message
    def render_error_message(self, value):
        if not value:
            return ""
        return mark_safe(value)

    class Meta:
        orderable = False
        template_name = "django_tables2/bootstrap4.html"
        # attrs = {"class": "table table-sm table-bordered", "style": "table-layout: fixed;"}
