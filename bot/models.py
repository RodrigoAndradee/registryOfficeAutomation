from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

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
    type = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PROCESSING')
    created_at = models.DateTimeField(default=timezone.now())
    finished_at = models.DateTimeField(null=True, blank=True)
    error_message = models.CharField(null=True, blank=True, max_length=510)
    can_retry = models.BooleanField(default=False)
