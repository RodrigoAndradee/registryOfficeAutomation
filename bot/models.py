from django.db import models
from django.utils import timezone
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
    type = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PROCESSING')
    created_at = models.DateTimeField(default=timezone.now)
