import json
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
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
        data = None 
        form = UploadJSONForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            try:
                data = json.load(uploaded_file)
                print("JSON CONTENT", json.dumps(data, indent=4, ensure_ascii=False))
            except json.JSONDecodeError:
                form.add_error('file', 'Arquivo JSON inválido.')
                return render(request, 'bot/automation_history.html', {'form': form, 'histories': histories})

            is_valid, error_msg = self.validate_json_fields(data)

            if not is_valid:
                messages.error(request, f"Erro de validação: {error_msg}", extra_tags="alert-danger")
                return redirect("history")
            
            form = UploadJSONForm()
            
            # Run automation
            for item in data["automation_data"]:
                instance = AutomationHistory.objects.create(
                    code = item["code"],
                    quantity = item["quantity"],
                    type = item["type"]
                )
                
                execute_form.delay(instance.id)
                # execute_form(instance.id)
                
            messages.success(request, "JSON importado com sucesso!", extra_tags="alert-success")
            return redirect("history")

        return render(request, 'bot/automation_history.html', {'form': form, 'data': data, 'histories': histories })
    
    def validate_json_fields(self, data):
        if "automation_data" not in data:
            return False, "Campo 'automation_data' está ausente."

        if not isinstance(data["automation_data"], list):
            return False, "'automation_data' deve ser uma lista."

        for i, item in enumerate(data["automation_data"]):
            if not isinstance(item, dict):
                return False, f"Item {i} em 'automation_data' deve ser um objeto."

            for campo in ["code", "quantity", "type"]:
                if campo not in item:
                    return False, f"Campo '{campo}' ausente no item {i}."

            if not isinstance(item["code"], str):
                return False, f"Campo 'code' no item {i} deve ser uma string."
            if not isinstance(item["quantity"], int):
                return False, f"Campo 'quantity' no item {i} deve ser um inteiro."
            if not isinstance(item["type"], str):
                return False, f"Campo 'type' no item {i} deve ser uma string."

        return True, ""
