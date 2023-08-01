from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Create your views here.
def home(request):
    return render(request, 'base.html')

def search(request):
    search_text = request.POST.get('search')
    search_content = {
        'search': search_text
    }
    return render(request, 'app/search.html', search_content)
