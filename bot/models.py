from django.db import models
from django.core.validators import RegexValidator

class AutomationHistory(models.Model):

    STATUS_CHOICES = [
        ('ERROR' , 'Erro'), 
        ('SUCCESS', 'Sucesso'), 
        ('PROCESSING', 'Processando')
    ]

    code = models.CharField(max_length=6,
        validators=[
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

class TypesOfTaxation(models.Model):
    code = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=512)
    mapped_value = models.IntegerField(null=True, blank=True)
    should_run_automation = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.description}"
