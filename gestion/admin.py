from django.contrib import admin
from .models import Cliente, Mascota

admin.site.register(Cliente)
admin.site.register(Mascota)
from .models import Consulta

admin.site.register(Consulta)

# Register your models here.
