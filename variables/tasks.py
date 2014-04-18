from celery import task
from variables.models import TimeSeries
import variables.automataconnect as connect
import datetime
from django.utils.timezone import utc
import datetime
from django.core.mail import send_mail



@task()
def store_value(server,name):
    value,quality,access_rights,time=connect.read(server,name)
    t = TimeSeries(server=server, name=name, value=value, time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    t.save()
    return 
    
@task()
def alarm(server,name,condition,value_limit,email):
    
    value,quality,access_rights,time=connect.read(server,name)    #Lectura del valor del ciente opc
    
    if condition=='greater':
        value_limit=float(value_limit)     #La variable se convierte de string a float
        value=float(value)     #La variable se convierte de string a float
        if  value > value_limit:
            send_mail('Online Scada Alarm', 'The variable ' + str(name) + ' on server ' + str(server) + ' is greater than its value limit '+ str(value_limit) + 
                      '. The actual value is '+str(value)+'.','onlinescadapfc@gmail.com',[str(email)], fail_silently=False)
    
    if condition=='less':
        value_limit=float(value_limit)     
        value=float(value)     

        if  value < value_limit:
            send_mail('Online Scada Alarm', 'The variable ' + str(name) + ' on server ' + str(server) + ' is lesser than its value limit '+ str(value_limit)+ 
                      '. The actual value is '+str(value)+'.','onlinescadapfc@gmail.com',['scandiskros@gmail.com'], fail_silently=False)
    
    if condition=='equal':
        value_limit=float(value_limit)     
        value=float(value)     
        if  value == value_limit:
            send_mail('Online Scada Alarm', 'The variable ' + str(name) + ' on server ' + str(server) + ' is equal to its limit '+ str(value_limit),
                      'onlinescadapfc@gmail.com',['scandiskros@gmail.com'], fail_silently=False)

    if condition=='not equal':
        value_limit=float(value_limit)     
        value=float(value)     
        if  value != value_limit:
            send_mail('Online Scada Alarm', 'The variable ' + str(name) + ' on server ' + str(server) + ' is not equal to '+ str(value_limit)+ 
                      '. The actual value is '+str(value)+'.','onlinescadapfc@gmail.com',['scandiskros@gmail.com'], fail_silently=False)
    return 
    
    
    