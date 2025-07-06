# gestion/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.nuevo_cliente, name='nuevo_cliente'),
    
path('mascotas/', views.lista_mascotas, name='lista_mascotas'),
    path('mascotas/nueva/', views.nueva_mascota, name='nueva_mascota'),

    path('mascotas/editar/<int:mascota_id>/', views.editar_mascota, name='editar_mascota'),
path('mascotas/eliminar/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),

path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),

path('consultas/', views.lista_consultas, name='lista_consultas'),
path('consultas/nueva/', views.nueva_consulta, name='nueva_consulta'),
 
path('mascotas/<int:mascota_id>/historial/', views.historial_mascota, name='historial_mascota'),

path('consultas/editar/<int:consulta_id>/', views.editar_consulta, name='editar_consulta'),
path('consultas/eliminar/<int:consulta_id>/', views.eliminar_consulta, name='eliminar_consulta'),
path('exportar/clientes_excel/', views.exportar_excel_clientes, name='exportar_clientes_excel'),
path('boleta/<int:cliente_id>/<int:mascota_id>/', views.boleta_pdf, name='boleta_pdf'),
path('boleta/consulta/<int:consulta_id>/', views.boleta_consulta_pdf, name='boleta_consulta_pdf'),

path('', views.inicio, name='inicio'),
    path('registro/', views.registro_usuario, name='registro'),
path('consultas/exportar/excel/', views.exportar_consultas_excel, name='exportar_consultas_excel'),
path('consultas/<int:consulta_id>/boleta/', views.generar_boleta_pdf, name='generar_boleta_pdf'),
path('mascotas/<int:mascota_id>/historial/pdf/', views.historial_mascota_pdf, name='historial_mascota_pdf'),





]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
