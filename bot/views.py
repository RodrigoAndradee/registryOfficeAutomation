import json
import logging
from datetime import datetime

from django.contrib import messages
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date

from bot.helpers.json_helpers.json_helper import split_chunks, validate_json_fields
from .models import AutomationHistory
from .forms import UploadJSONForm
from .tasks import execute_form

logger = logging.getLogger(__name__)

class ListHistory(View):

    def render_history(self, request: HttpRequest, form: UploadJSONForm, histories) -> HttpResponse:
        return render(request, 'bot/automation_history.html', {
            'form': form, 
            'histories': histories
        })

    def get(self, request: HttpRequest) -> HttpResponse:
        status = request.GET.get("status")
        date_str = request.GET.get("date")
        form: UploadJSONForm = UploadJSONForm()

        histories = AutomationHistory.objects.all()

        if status:
            histories = histories.filter(status=status)
        if date_str:
            parsed_date = parse_date(date_str)
            if parsed_date:
                histories = histories.filter(created_at=parsed_date)
            else:
                messages.warning(request, "Formato de data inválido", extra_tags="alert-warning")

        return self.render_history(request, form, histories)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        form: UploadJSONForm = UploadJSONForm(request.POST, request.FILES)
        histories = AutomationHistory.objects.all()

        if not form.is_valid():
            return self.render_history(request, form, histories)

        uploaded_file = form.cleaned_data['file']

        try:
            json_content = json.load(uploaded_file)
        except json.JSONDecodeError as e:
            logger.error("Erro ao carregar JSON: %s", e)
            form.add_error('file', 'Arquivo JSON inválido.')
            return self.render_history(request, form, histories)

        error_msg, valid_fields, invalid_fields = validate_json_fields(json_content)

        # Checking if there is no valid data
        if len(valid_fields) == 0:
            messages.error(request, f"Erro de validação: {error_msg}", extra_tags="alert-danger")
            return redirect("history")
        
        for item in valid_fields:
            instance = AutomationHistory.objects.create(
                code=item["code"],
                quantity=item["quantity"],
                type=item["type"]
            )
            item["item_id"] = instance.id

        for chunk in split_chunks(valid_fields):
            execute_form.delay(chunk)

        messages.success(request, f"JSON importado com sucesso! {len(valid_fields)} ite{'ns' if len(valid_fields) > 1 else 'm'} importado(s) com sucesso e {len(invalid_fields)} ite{'ns' if len(invalid_fields) > 1 else 'm'} inválido(s)!", extra_tags="alert-success")
        return redirect("history")
