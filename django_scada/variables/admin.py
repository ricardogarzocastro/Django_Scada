from variables.models import Variable
from django.contrib import admin
from django import forms
#For peeking at the queue in Django's database
from kombu.transport.django import models as kombu_models
admin.site.register(kombu_models.Message)


class VariableAdmin(admin.ModelAdmin):
    fieldsets = [
        ('OPC Server',               {'fields': ['server']}),
        ('Variable Name', {'fields': ['name']}),
    ]
    list_display = ('name','server')
    search_fields = ['server','name']
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(VariableAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.user.id:
            return False
        return True
    
    def queryset(self, request):
        if request.user.is_superuser:
            return Variable.objects.all()
        return Variable.objects.filter(user=request.user)

    def save_model(self, request, obj, form, change): 
        obj.user = request.user
        obj.save()
        
admin.site.register(Variable,VariableAdmin)