from django.conf.urls import *
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home/', 'variables.views.home'),
    #Url del manual de usuario
    url(r'^manual/', 'variables.views.manual'),
    #Url de lecutras de vairable
    url(r'^read/', 'variables.views.read'),
    #Url para enviar datos mediante HTTP Request para refrescar variables
    url(r'^json/read_update/','variables.views.read_update'),
    #Url de escritura de variables
    url(r'^control/','variables.views.control'),
    #Url para enviar datos mediante HTTP Request para escribir variables
    url(r'^json/control_response/',  'variables.views.control_response'),
    #Url para selecionar las variables a mostrar
    url(r'^display_editor/','variables.views.display_editor'), 
    #Url para intercambio de datos cliente-navegador mediante HTTP Request
    url(r'^json/display_editor_response/',  'variables.views.display_editor_response'),
    #Url para la pagina con la grafica para variables
    url(r'^graph_live/', 'variables.views.graph_live'),
    #Url de intercambio asincrono de datos para la grafica mediante HTTP Request
    url(r'^json/graph_live/',  'variables.views.json_graph_live'),
    #Url para mostrar la grafica de representacion historica de variables
    url(r'^graph_db/', 'variables.views.graph_db'), 
    #Url para intercambio de datos mediante HTTP Request de la grafica historica
    url(r'^json/graph_db/',  'variables.views.json_query_db'),    
    #Url para crear una tabla con los valores historicos de variables
    url(r'^log_db/', 'variables.views.log_db'), 
    #Url para intecambio de datos mediante HTTP Request para la tabla de valores historicos
    url(r'^json/log_db/',  'variables.views.json_query_db'),
    #Url de django para el menu de administrador
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #Url para login y logout de usuario
    url('^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/login/'}),
                      
    url(r'', include('django.contrib.auth.urls')),


)


urlpatterns += staticfiles_urlpatterns()
'''
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL[1:-1],
         'django.views.static.serve',
         {'document_root':  settings.MEDIA_ROOT, 'show_indexes': True}),
    )
    '''