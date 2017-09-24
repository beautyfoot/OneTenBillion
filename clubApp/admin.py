from django.contrib import admin

# Register your models here.


from clubApp.models import League, Club
from playApp.models import Play


admin.site.register(League)
admin.site.register(Club)
admin.site.register(Play)
