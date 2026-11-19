from django.http import HttpResponse
from django.shortcuts import render


def aboutUS(request):
    return HttpResponse("Welcome to QuiCo")

