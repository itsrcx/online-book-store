from django.shortcuts import render
from django.views import generic

def homeView(request):
    context = {'list': [1,2,3,4,5,6,7,8,9,10]}
    return render(request, 'index.html', context)

def cartView(request):
    context = {}
    return render(request, 'index.html', context)

def checkoutView(request):
    context = {}
    return render(request, 'index.html', context)