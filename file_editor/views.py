from django.shortcuts import render, redirect
from django.views import View

from .forms import PostForm

class FileEditor(View):

    def post(self, request):
        form = PostForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return redirect("success")
        
        return render(request, "file_editor/file_editor.html", {"form": form})
    

    def get(self, request):
        form = PostForm(request.POST)
        return render(request, "file_editor/file_editor.html", {"form": form})
