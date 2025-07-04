import json
import logging
from datetime import datetime
from copy import deepcopy

from django.contrib import messages
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django_tables2 import RequestConfig

from .models import AutomationHistory, TypesOfTaxation
from .tables import AutomationHistoryTable, HistoryDetailsTable
from .forms import UploadJSONForm
from .tasks import execute_form

from bot.helpers.json_helpers.json_helper import split_chunks, validate_json_fields

logger = logging.getLogger(__name__)

class ListHistory(View):
    
    @staticmethod
    def serialize_invalid_fields(fields):
        serialized = []
        for item in fields:
            item_copy = deepcopy(item)
            for key, value in item_copy.items():
                if isinstance(value, datetime):
                    item_copy[key] = value.isoformat()
            serialized.append(item_copy)
        return serialized
    
    @staticmethod
    def render_history(request: HttpRequest, form: UploadJSONForm, histories) -> HttpResponse:
        table = AutomationHistoryTable(histories)
        RequestConfig(request, paginate={"per_page": 30}).configure(table)

        show_history_details_modal = request.session.pop("show_history_details_modal", False)
        invalid_data = request.session.pop("invalid_fields", None)
        history_details_table = HistoryDetailsTable(invalid_data) if invalid_data else None
        current_year = datetime.now().year

        return render(request, "bot/automation_history.html", {
            "form": form,
            "histories": histories,
            "table": table,
            "show_history_details_modal": show_history_details_modal,
            "history_details_table": history_details_table,
            "current_year": current_year,
        })

    def get(self, request: HttpRequest) -> HttpResponse:
        status = request.GET.get("status")
        month = request.GET.get("month")
        year = request.GET.get("year")

        form: UploadJSONForm = UploadJSONForm()

        histories = AutomationHistory.objects.all().order_by("-id")

        if status:
            histories = histories.filter(status=status)
        if month:
            histories = histories.filter(month_of_competence=month)
        if year:
            histories = histories.filter(year_of_competence=year)

        return self.render_history(request, form, histories)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        form: UploadJSONForm = UploadJSONForm(request.POST, request.FILES)
        month = request.POST.get("month")
        histories = AutomationHistory.objects.all().order_by("-id")
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
            
            # Saving the "no need to run" or "has some error" to show to user on the table
            if invalid_fields:
                for item in invalid_fields:
                    item["month_of_competence"] = month
                    instance = AutomationHistory.objects.create(**item)
                    
                request.session["show_history_details_modal"]= True
                request.session["invalid_fields"] = self.serialize_invalid_fields(invalid_fields)
            
            # Running the automation on the data that is safe to run
            if valid_fields:
                for item in valid_fields:
                    item["month_of_competence"] = month
                    instance = AutomationHistory.objects.create(**item)
                    item["item_id"] = instance.id
                
                for chunk in split_chunks(valid_fields):
                    execute_form.delay(chunk, month)
                
                # messages.success(request, f"{len(valid_fields)} ite{'ns' if len(valid_fields) > 1 else 'm'} importado(s) com sucesso e {len(invalid_fields)} ite{'ns' if len(invalid_fields) > 1 else 'm'} inválido(s)!", extra_tags="success")
                            
            elif not invalid_fields:
                messages.error(request, "Nenhum dado válido no JSON.", extra_tags="danger")
                
        except Exception as e:
            print(e)
            messages.error(request, e, extra_tags="danger")
            return self.render_history(request, form, histories)
        
        # Returning the updated values on the table
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
