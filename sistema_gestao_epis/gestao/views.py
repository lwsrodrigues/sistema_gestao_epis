from django.http import HttpResponse

def home(request):
    return HttpResponse("Bem-vindo ao sistema de gestão!")
