
from django.shortcuts import redirect

def index_view(request):
    return redirect('register')
