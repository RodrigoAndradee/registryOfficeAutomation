import json
import logging
from datetime import datetime

from django.contrib import messages
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django_tables2 import RequestConfig

from .models import AutomationHistory, TypesOfTaxation
from .tables import AutomationHistoryTable
from .forms import UploadJSONForm
from .tasks import execute_form

from bot.helpers.json_helpers.json_helper import split_chunks, validate_json_fields

logger = logging.getLogger(__name__)

class ListHistory(View):
    
    def render_history(self, request: HttpRequest, form: UploadJSONForm, histories) -> HttpResponse:
        table = AutomationHistoryTable(histories)
        RequestConfig(request, paginate={"per_page": 30}).configure(table)

        return render(request, "bot/automation_history.html", {
            "form": form, 
            "histories": histories,
            "table": table
        })

    def get(self, request: HttpRequest) -> HttpResponse:
        status = request.GET.get("status")
        date_str = request.GET.get("date")

        form: UploadJSONForm = UploadJSONForm()

        histories = AutomationHistory.objects.all().order_by("-id")

        if status:
            histories = histories.filter(status=status)
        if date_str:
            parsed_date = parse_date(date_str)
            if parsed_date:
                start_datetime = datetime.combine(parsed_date, datetime.min.time())
                end_datetime = datetime.combine(parsed_date, datetime.max.time())
                histories = histories.filter(created_at__range=(start_datetime, end_datetime))
            else:
                messages.warning(request, "Formato de data inválido", extra_tags="danger")

        return self.render_history(request, form, histories)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        form: UploadJSONForm = UploadJSONForm(request.POST, request.FILES)
        histories = AutomationHistory.objects.all()
        taxation_types = list(TypesOfTaxation.objects.all())
    
        if not form.is_valid():
            return self.render_history(request, form, histories)

        uploaded_file = form.cleaned_data["file"]

        if uploaded_file.content_type != 'application/json':
            form.add_error('file', 'O tipo de arquivo não é JSON.')
            messages.warning(request, "O tipo de arquivo não é JSON.'", extra_tags="danger")
            return self.render_history(request, form, histories)

        try:
            json_content = json.load(uploaded_file)
        except json.JSONDecodeError as e:
            form.add_error("file", "Arquivo JSON inválido.")
            return self.render_history(request, form, histories)

        try:
            valid_fields, invalid_fields = validate_json_fields(json_content, taxation_types)
            
            print(valid_fields)
            print(invalid_fields)
        except Exception as e:
            print(e)
            form.add_error("file", f"Arquivo JSON inválido. {e}")
            
            
        
            
        # Checking if there is no valid data
        # if len(valid_fields) == 0:
        #     messages.error(request, error_msg if error_msg else "Nenhum dado importado corretamente! Verifique seu JSON!", extra_tags="danger")
        #     return redirect("history")
        
        # for item in valid_fields:
        #     instance = AutomationHistory.objects.create(
        #         code=item["code"],
        #         quantity=item["quantity"],
        #         type=item["type"]
        #     )
        #     item["item_id"] = instance.id

        # for chunk in split_chunks(valid_fields):
        #     execute_form.delay(chunk)

        # messages.success(request, f"{len(valid_fields)} ite{'ns' if len(valid_fields) > 1 else 'm'} importado(s) com sucesso e {len(invalid_fields)} ite{'ns' if len(invalid_fields) > 1 else 'm'} inválido(s)!", extra_tags="success")
        return redirect("history")
    
class RetryHistory(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get("pk")
    
        if pk is not None:
            history = get_object_or_404(AutomationHistory, pk=pk)

            if history.status == "ERROR":
                history_copy = {
                    "code": history.code,
                    "quantity": history.quantity,
                    "type": history.type,
                    "item_id": history.id
                }

                instance = AutomationHistory.objects.create(
                    code=history_copy["code"],
                    quantity=history_copy["quantity"],
                    type=history_copy["type"]
                )
                history_copy["item_id"] = instance.id

                # Removing the retry button from the original row
                history.can_retry = False
                history.save()

                execute_form.delay([history_copy])
                messages.success(request, "Tarefa reenviada com sucesso.", extra_tags="success")
        
        return redirect("history")
