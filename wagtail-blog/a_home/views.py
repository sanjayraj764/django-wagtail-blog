from django.shortcuts import render, redirect

def home_view(request):
    context = {}
    return redirect('blog/')