from django.shortcuts import render
from cassia_automation import main


def index(request):
    return render(request,'index.html')

def function(request):
    return render(request,'func.html')

def run(request):
    return render(request,'run.html',)
