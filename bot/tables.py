from django.utils.html import format_html
from django.urls import reverse

import django_tables2 as tables

from bot.models import AutomationHistory

class AutomationHistoryTable(tables.Table):
    status = tables.Column(verbose_name="Status")
    created_at = tables.DateTimeColumn(format="d/m/Y H:i", verbose_name="Criado em")
    finished_at = tables.DateTimeColumn(format="d/m/Y H:i", verbose_name="Finalizado em")
    action = tables.TemplateColumn(template_name="bot/automation_history_actions_column.html", verbose_name="Ações")

    def render_status(self, record):
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
            }.get(status, format_html('<i class="bi bi-arrow-repeat me-1 spinner-grow spinner-grow-sm"></i>'))
        
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
        