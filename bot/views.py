from django.http import JsonResponse
from .tasks import execute_form
from django.views import View


class RunBot(View):

    def get(self, request):
        task = execute_form.delay() # runs this process without blocking the django execution
        return JsonResponse({"task_id": task.id})

    
