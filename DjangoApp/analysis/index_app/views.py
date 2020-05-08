from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# from .models import Question, Choice

def index_page(request):
    return render(request,'index_app/index.html')
