from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse

from django.template.loader import render_to_string

from weasyprint import HTML
from .models import Post

from .forms import PostForm

class FileEditor(View):
    
    def export_pdf(request, post_id):
        post = get_object_or_404(Post, id=post_id)
        html_string = render_to_string("file_editor/file_editor.html", { "post": post })
        html = HTML(string=html_string)
        
        pdf_file = html.white_pdf()
        
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f"filename=post_{post.id}.pdf"
        return response

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data["title"]
            
            print(post)
            
            html_string = render_to_string("export_pdf/export_pdf.html", {"post": post})
            pdf_file = HTML(string=html_string).write_pdf()

            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = f"attachment; filename={title}.pdf"
            return response
            
        else :
            form = PostForm()
        return render(request, "file_editor/file_editor.html", {"form": form})
    

    def get(self, request):
        form = PostForm(request.POST)
        return render(request, "file_editor/file_editor.html", {"form": form})
