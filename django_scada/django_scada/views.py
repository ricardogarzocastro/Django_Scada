from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login')