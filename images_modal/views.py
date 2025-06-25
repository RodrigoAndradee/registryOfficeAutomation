from django.shortcuts import render
from django.views import View

class FirstBook(View):
    def get(self, request): 

        images = [
            {"url": "https://letsenhance.io/static/73136da51c245e80edc6ccfe44888a99/1015f/MainBefore.jpg"},
            {"url": "https://gru.ifsp.edu.br/images/phocagallery/galeria2/image03_grd.png"},
        ]
        return render(request, "book_1/book_1.html", {"images": images})
    
    def post(self, request):
        print(request);
        
        images = [
                {"url": "https://letsenhance.io/static/73136da51c245e80edc6ccfe44888a99/1015f/MainBefore.jpg"},
                {"url": "https://gru.ifsp.edu.br/images/phocagallery/galeria2/image03_grd.png"},
            ]

        return render(request, "book_1/book_1.html", {"images": images})

class SecondBook(View):
    def get(self, request): 

        images = [
            {"url": "https://letsenhance.io/static/73136da51c245e80edc6ccfe44888a99/1015f/MainBefore.jpg"},
            {"url": "https://gru.ifsp.edu.br/images/phocagallery/galeria2/image03_grd.png"},
            {"url": "https://static.vecteezy.com/ti/fotos-gratis/t2/36324708-ai-gerado-cenario-do-uma-tigre-caminhando-dentro-a-floresta-foto.jpg"},
            {"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT87L9hJmLkLymJ7ACCsQg8v6J6b-Hm2v1ZJA&s"},
        ]
        return render(request, "book_2/book_2.html", {"images": images})
    
    def post(self, request):
        print(request);
        
        images = [
            {"url": "https://letsenhance.io/static/73136da51c245e80edc6ccfe44888a99/1015f/MainBefore.jpg"},
            {"url": "https://gru.ifsp.edu.br/images/phocagallery/galeria2/image03_grd.png"},
        ]

        return render(request, "book_2/book_2.html", {"images": images})
