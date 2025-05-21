import os
import json
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from bot.helpers.json_helpers.json_helper import split_chunks, validate_json_fields
from .models import AutomationHistory
from .forms import UploadJSONForm
from .tasks import execute_form

class ListHistory(View):

    def get(self, request):
        form = UploadJSONForm()
        histories = AutomationHistory.objects.all()
        return render(request, 'bot/automation_history.html', {"histories": histories , 'form': form})
    
    def post(self, request):
        histories = AutomationHistory.objects.all()
        json_content = None 
        form = UploadJSONForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data['file']

            try:
                json_content = json.load(uploaded_file)
            except json.JSONDecodeError:
                form.add_error('file', 'Arquivo JSON inválido.')
                return render(request, 'bot/automation_history.html', {'form': form, 'histories': histories})

            is_valid, error_msg = validate_json_fields(json_content)

            if not is_valid:
                messages.error(request, f"Erro de validação: {error_msg}", extra_tags="alert-danger")
                return redirect("history")
            
            form = UploadJSONForm()

            # Adding the initial data to the database
            for item in json_content["automation_data"]:
                instance = AutomationHistory.objects.create(
                    code = item["code"],
                    quantity = item["quantity"],
                    type = item["type"]
                )
                item["item_id"] = instance.id

            json_chunks = split_chunks(json_content["automation_data"])
            
            # Run automation
            for chunk in json_chunks:
                execute_form.delay(chunk)
                
            messages.success(request, "JSON importado com sucesso!", extra_tags="alert-success")
            return redirect("history")

        return render(request, 'bot/automation_history.html', {'form': form, 'histories': histories })
