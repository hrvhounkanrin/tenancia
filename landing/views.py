"""landing views."""
from django.shortcuts import render


def index(request):
    """Landing index."""
    return render(request, 'home.html')
