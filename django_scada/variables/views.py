# -*- coding: utf-8 -*- 
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db import models
from variables.models import Variable, TimeSeries
import variables.automataconnect as connect
from django.views.decorators.csrf import csrf_exempt 
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import json
from django.utils import simplejson
import datetime

def check_json_data(request):

    if request.method == 'POST':
        json_data = simplejson.loads(request.body)
    try:
        data = json_data['data'][0]
        return data
    except KeyError:
        return HttpResponseServerError("Malformed data!")

@login_required
def json_query_db(request):
    data=check_json_data(request)
    #Consultas a la base de datos y filtrado de los datos obtenidos.
    response_json_data={"TimeSeries":[]}
    q=TimeSeries.objects.all()
    q=q.filter(server=data['server'])
    q=q.filter(name=data['name'])
    to_year=int(data['to-year'],base=10)
    to_month=int(data['to-month'],base=10)
    to_day=int(data['to-day'],base=10)
    from_year=int(data['from-year'],base=10)
    from_month=int(data['from-month'],base=10)
    from_day=int(data['from-day'],base=10)
    q=q.exclude(time__gte=datetime.datetime(to_year,to_month,to_day))
    q=q.filter(time__gte=datetime.datetime(from_year,from_month,from_day))
    q=q.order_by('time')
    #Transfomar la variable que se encuentra en un formato propio de la base de datos a un diccionario python.
    if not q:
        dict={}
        dict['value']='None';
        dict['time']="None";
        response_json_data['TimeSeries'].append(dict)
    else:
        for e in q:
            print e.server,e.name,e.value,e.time
            
            dict={}
            dict['value']=e.value
            dict['time']=e.time
            response_json_data['TimeSeries'].append(dict)
    return HttpResponse(json.dumps(response_json_data, cls=DjangoJSONEncoder), mimetype='application/json')

def json_graph_live (request):
    if request.method == 'POST':
        json_data = simplejson.loads(request.body)
    try:
        data = json_data['data'][0]
    except KeyError:
        return HttpResponseServerError("Malformed data!")
    data=check_json_data(request)
    dict={}
    dict['value'],dict['quality'],access_rights,dict['time']=connect.read(data['server'],data['name'])
    
    return HttpResponse(json.dumps(dict), mimetype='application/json')

@login_required
def read_update(request):
    json_data={"variables":[]}
    variable_list=get_variables(request.user)
    for e in variable_list:
        dict={}
        dict['server']=e.server
        dict['name']=e.name
        dict['value'],dict['quality'],dict['access_rights'],time=connect.read(e.server,e.name)
        json_data['variables'].append(dict)    
    return HttpResponse(json.dumps(json_data), mimetype='application/json')

@permission_required('variables.change_Variable',raise_exception=True)
def control_response (request):
    #Verifica si los datos de la petición HTTP son correctos.
    if request.method == 'POST':
        json_data = simplejson.loads(request.body)
    try:
        data = json_data['data'][0]
    except KeyError:
        return HttpResponseServerError("Malformed data!")
    #Crea vector con datos de respuesta
    response_array=[]
    i=0
    while i<len(json_data['data']):
        server,name,value=json_data['data'][i]['server'],json_data['data'][i]['name'],json_data['data'][i]['value']
        response_array=connect.write(server,name,value,response_array)
        i=i+1
    return HttpResponse(json.dumps(response_array), mimetype='application/json')

@login_required
def display_editor_response(request):    
    if request.method == 'POST':
        json_data_dict = simplejson.loads(request.body)
    try:
        data = json_data_dict['data'][0]
    except KeyError:
        return HttpResponseServerError("Malformed data!")
    response_array=[]
    variable_list=Variable.objects.filter(user=request.user)
    print variable_list
    for data in json_data_dict['data']:
        q=variable_list.filter(name=data['name'])
        q=q.filter(server=data['server'])
        for variable in q:
            variable.display=data['display']
            variable.save()
            print variable.display
    return HttpResponse(json.dumps(response_array), mimetype='application/json')

def variable_list_django_db(user):
    server_list=[]
    raw_variable_list=Variable.objects.filter(user=user)
    variable_list = []
    for e in raw_variable_list:
        i=0
        encontrado=False
        while i<len(variable_list):
            if variable_list[i].server==e.server and variable_list[i].name==e.name:
                encontrado=True
                break
            else:
                encontrado=False
                i=i+1
        if not encontrado:
            variable_list.append(e)    
            
    return variable_list

def get_variables(user):
    variable_list=variable_list_django_db(user)
    i=0
    while i<len(variable_list):
        variable_list[i].value,variable_list[i].quality,variable_list[i].access_rights,time=connect.read(variable_list[i].server,variable_list[i].name)
        i=i+1
    return variable_list

def get_writable_variables(user):
    variable_list=variable_list_django_db(user)
    i=0
    while i<len(variable_list):
        variable_list[i].value,variable_list[i].quality,variable_list[i].access_rights,time=connect.read(variable_list[i].server,variable_list[i].name)
        if variable_list[i].access_rights =='Read':
            del variable_list[i]
        i=i+1

    return variable_list

@login_required
def home(request):
    return render_to_response('home.html',context_instance=RequestContext(request))

@login_required
def manual(request):
    return render_to_response('manual.html',context_instance=RequestContext(request))

@login_required
def read(request):  
    variable_list=get_variables(request.user)    
    return render_to_response('read.html', {'variable_list': variable_list} , context_instance=RequestContext(request))

@login_required
def control(request):  
    variable_list=get_writable_variables(request.user)    
    return render_to_response('control.html', {'variable_list': variable_list} , context_instance=RequestContext(request))

@login_required
def display_editor(request):
    variable_list=get_variables(request.user)    
    return render_to_response('display_editor.html', {'variable_list': variable_list} , context_instance=RequestContext(request))

@login_required
def graph_live(request):   
    variable_list=get_variables(request.user)    
    return render_to_response('graph_live.html', {'variable_list': variable_list} , context_instance=RequestContext(request))

@login_required
def graph_db(request):
    variable_list=get_variables(request.user)    
    return render_to_response('graph_db.html', {'variable_list': variable_list} , context_instance=RequestContext(request)) 

@login_required
def log_db(request):
    variable_list=get_variables(request.user)    
    return render_to_response('log_db.html', {'variable_list': variable_list} , context_instance=RequestContext(request)) 



##############################





