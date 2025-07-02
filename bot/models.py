from datetime import datetime

from django.db import models
from django.core.validators import RegexValidator

class AutomationHistory(models.Model):
    
    def previous_month():
        month = datetime.now().month - 1
        return str(month if month > 0 else 12)
    
    def current_year():
        return str(datetime.now().year)

    STATUS_CHOICES = [
        ('ERROR' , 'Erro'), 
        ('SUCCESS', 'Sucesso'), 
        ('PROCESSING', 'Processando')
    ]
    
    MONTHS_CHOICES = [(str(i), nome) for i, nome in enumerate([
        '', 
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro'
    ]) if i > 0]
    
    code = models.CharField(max_length=6, validators=[
            RegexValidator(
                regex=r'^\d{4}-\d$',
                message='O código deve estar no formato 9999-9.',
                code='invalid_code'
            )
        ])
    quantity = models.IntegerField()
    type =  models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PROCESSING')
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error_message = models.CharField(null=True, blank=True, max_length=1024)
    can_retry = models.BooleanField(default=False)
    mapped_type = models.IntegerField(null=True, blank=True)
    month_of_competence = models.CharField(max_length=2, choices=MONTHS_CHOICES, default=previous_month)
    year_of_competence = models.CharField(max_length=4, validators=[
            RegexValidator(
                regex=r'^\d{4}',
                message='O código deve estar no formato 9999.',
                code='incorrect_year_of_competence'
            ),
        ], default=current_year)

class TypesOfTaxation(models.Model):
    type = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=512)
    mapped_type = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.description}"
