from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Mascota, Consulta
from .forms import ClienteForm, MascotaForm, ConsultaForm
from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import datetime
import openpyxl
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import io
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth import login
from .forms import RegistroUsuarioForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncDate
from django.utils import timezone
import calendar
# -------------------- CLIENTES --------------------
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'gestion/clientes.html', {'clientes': clientes})

@login_required
def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'gestion/cliente_form.html', {'form': form})

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect('lista_clientes')
    return render(request, 'gestion/cliente_form.html', {'form': form})

@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'gestion/confirmar_eliminar.html', {'objeto': cliente, 'tipo': 'cliente'})

# -------------------- MASCOTAS --------------------
@login_required
def lista_mascotas(request):
    mascotas = Mascota.objects.select_related('cliente').all()
    return render(request, 'gestion/mascotas.html', {'mascotas': mascotas})

@login_required
def nueva_mascota(request):
    form = MascotaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_mascotas')
    return render(request, 'gestion/mascota_form.html', {'form': form})

@login_required
def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    form = MascotaForm(request.POST or None, instance=mascota)
    if form.is_valid():
        form.save()
        return redirect('lista_mascotas')
    return render(request, 'gestion/mascota_form.html', {'form': form})

@login_required
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    if request.method == 'POST':
        mascota.delete()
        return redirect('lista_mascotas')
    return render(request, 'gestion/confirmar_eliminar.html', {'objeto': mascota, 'tipo': 'mascota'})

# -------------------- CONSULTAS --------------------
@login_required
def lista_consultas(request):
    consultas = Consulta.objects.select_related('mascota', 'mascota__cliente').order_by('-fecha')
    return render(request, 'gestion/consultas.html', {'consultas': consultas})

@login_required
def nueva_consulta(request):
    form = ConsultaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_consultas')
    return render(request, 'gestion/consulta_form.html', {'form': form})

@login_required
def editar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    form = ConsultaForm(request.POST or None, instance=consulta)
    if form.is_valid():
        form.save()
        return redirect('lista_consultas')
    return render(request, 'gestion/consulta_form.html', {'form': form})

@login_required
def eliminar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == 'POST':
        consulta.delete()
        return redirect('lista_consultas')
    return render(request, 'gestion/confirmar_eliminar.html', {'objeto': consulta, 'tipo': 'consulta'})

@login_required
def historial_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    consultas = Consulta.objects.filter(mascota=mascota).order_by('-fecha')
    return render(request, 'gestion/historial_mascota.html', {
        'mascota': mascota,
        'consultas': consultas
    })

# -------------------- DASHBOARD --------------------
@login_required
def inicio(request):
    # --- Filtros ---
    hoy = timezone.now()
    # Obtener todos los años disponibles en la base de datos
    años_disponibles = [d.year for d in Consulta.objects.dates('fecha', 'year', order='DESC')]
    año_actual = int(request.GET.get('año', hoy.year))
    # Obtener todas las especies disponibles
    especies_disponibles = Mascota.objects.values_list('especie', flat=True).distinct()
    especie_actual = request.GET.get('especie', '')

    # --- QuerySet base filtrado ---
    consultas_qs = Consulta.objects.filter(fecha__year=año_actual)
    if especie_actual:
        consultas_qs = consultas_qs.filter(mascota__especie=especie_actual)

    # Consultas por mes
    consultas_por_mes = (
        consultas_qs
        .annotate(mes=TruncMonth('fecha'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )
    meses = []
    consultas_por_mes_data = []
    for item in consultas_por_mes:
        mes_num = item['mes'].month
        meses.append(calendar.month_name[mes_num])
        consultas_por_mes_data.append(item['total'])

    # Consultas por especie
    consultas_por_especie = (
        consultas_qs.select_related('mascota')
        .values('mascota__especie')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    especies = [item['mascota__especie'] for item in consultas_por_especie]
    consultas_por_especie_data = [item['total'] for item in consultas_por_especie]

    # Clientes con más mascotas (top 10)
    clientes_qs = Cliente.objects.annotate(num_mascotas=Count('mascota')).filter(num_mascotas__gt=0).order_by('-num_mascotas')[:10]
    clientes = [c.nombre for c in clientes_qs]
    mascotas_por_cliente = [c.num_mascotas for c in clientes_qs]

    # Matriz de días por mes
    consultas_por_dia = (
        consultas_qs
        .annotate(fecha_dia=TruncDate('fecha'))
        .values('fecha_dia')
        .annotate(total=Count('id'))
        .order_by('fecha_dia')
    )
    matriz_datos = {}
    for item in consultas_por_dia:
        fecha = item['fecha_dia']
        mes = fecha.strftime('%B')
        dia = fecha.day
        matriz_datos.setdefault(mes, {})[dia] = item['total']

    contexto = {
        'años_disponibles': años_disponibles,
        'año_actual': año_actual,
        'especies_disponibles': especies_disponibles,
        'especie_actual': especie_actual,
        'meses': meses,
        'consultas_por_mes': consultas_por_mes_data,
        'especies': especies,
        'consultas_por_especie': consultas_por_especie_data,
        'clientes': clientes,
        'mascotas_por_cliente': mascotas_por_cliente,
        'matriz_datos': matriz_datos,
    }
    return render(request, 'gestion/inicio.html', contexto)

# -------------------- EXCEL EXPORT --------------------
@login_required
def exportar_excel_clientes(request):
    clientes = (
        Cliente.objects
        .annotate(num_mascotas=Count('mascota'))
        .filter(num_mascotas__gt=0)
        .order_by('-num_mascotas')[:10]
    )
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Top Clientes"
    ws.append(['Cliente', 'Cantidad de Mascotas'])
    for cliente in clientes:
        ws.append([cliente.nombre, cliente.num_mascotas])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=top_clientes_mascotas.xlsx'
    wb.save(response)
    return response

# -------------------- PDF BOLETAS --------------------
@login_required
def boleta_pdf(request, cliente_id, mascota_id):
    cliente = Cliente.objects.get(id=cliente_id)
    mascota = Mascota.objects.get(id=mascota_id)

    conceptos = [
        {'descripcion': 'Consulta veterinaria', 'monto': 50.00},
        {'descripcion': 'Vacuna antirrábica', 'monto': 30.00},
        {'descripcion': 'Desparasitación', 'monto': 20.00}
    ]
    total = sum(item['monto'] for item in conceptos)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="boleta.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo_unmsm.png')
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        p.drawImage(logo, 50, 700, width=80, height=80, preserveAspectRatio=True)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(150, 750, "Veterinaria Perrovaca UNMSM")
    p.setFont("Helvetica", 12)
    p.drawString(150, 735, "Boleta de Venta")
    p.drawString(400, 735, f"Fecha: {datetime.today().strftime('%d/%m/%Y')}")

    p.drawString(50, 690, f"Cliente: {cliente.nombre}")
    p.drawString(50, 670, f"Mascota: {mascota.nombre} ({mascota.especie} - {mascota.raza})")

    y = 630
    p.drawString(50, y, "Descripción")
    p.drawString(400, y, "Monto (S/)")
    y -= 20
    for item in conceptos:
        p.drawString(50, y, item['descripcion'])
        p.drawString(400, y, f"{item['monto']:.2f}")
        y -= 20

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y - 10, "TOTAL")
    p.drawString(400, y - 10, f"S/ {total:.2f}")
    p.showPage()
    p.save()
    return response

@login_required
def boleta_consulta_pdf(request, consulta_id):
    consulta = Consulta.objects.select_related('mascota__cliente').get(id=consulta_id)
    mascota = consulta.mascota
    cliente = mascota.cliente

    conceptos = [{'descripcion': f'Consulta: {consulta.motivo}', 'monto': 50.00}]
    if consulta.tratamiento:
        conceptos.append({'descripcion': 'Tratamiento aplicado', 'monto': 30.00})
    if consulta.observaciones:
        conceptos.append({'descripcion': 'Observaciones clínicas', 'monto': 20.00})
    total = sum(item['monto'] for item in conceptos)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo_unmsm.png')
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        p.drawImage(logo, 50, 700, width=80, height=80, preserveAspectRatio=True)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(150, 750, "Veterinaria UNMSM")
    p.setFont("Helvetica", 12)
    p.drawString(150, 735, "Boleta de Consulta Veterinaria")
    p.drawString(400, 735, f"Fecha: {consulta.fecha.strftime('%d/%m/%Y')}")

    p.drawString(50, 700, f"Cliente: {cliente.nombre}")
    p.drawString(50, 680, f"Mascota: {mascota.nombre} ({mascota.especie})")

    y = 640
    p.drawString(50, y, "Descripción")
    p.drawString(400, y, "Monto (S/)")
    y -= 20
    for item in conceptos:
        p.drawString(50, y, item['descripcion'])
        p.drawString(400, y, f"{item['monto']:.2f}")
        y -= 20

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y - 10, "TOTAL")
    p.drawString(400, y - 10, f"S/ {total:.2f}")

    p.showPage()
    p.save()
    pdf_value = buffer.getvalue()
    filename = f"boleta_consulta_{consulta.id}.pdf"
    consulta.boleta_pdf.save(filename, ContentFile(pdf_value))
    buffer.close()

    response = HttpResponse(pdf_value, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

# -------------------- USUARIO --------------------
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'gestion/registro.html', {'form': form})

from django.db.models.functions import ExtractMonth

consultas_por_mes = (
    Consulta.objects
    .filter(fecha__year=2025)
    .annotate(mes=ExtractMonth('fecha'))
    .values('mes')
    .annotate(total=Count('id'))
    .order_by('mes')
)

meses = []
totales = []
for item in consultas_por_mes:
    mes_num = item['mes']
    meses.append(calendar.month_name[mes_num])
    totales.append(item['total'])
# En tu archivo forms.py

from django import forms
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['mascota', 'fecha', 'motivo', 'diagnostico', 'tratamiento']
        widgets = {
            'mascota': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Vacunación anual, cojera, etc.'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe el diagnóstico profesional...'}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe el tratamiento a seguir...'}),
        }
import openpyxl
from django.http import HttpResponse

def exportar_consultas_excel(request):
    consultas = Consulta.objects.select_related('mascota', 'mascota__cliente').order_by('-fecha')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Consultas"

    # Encabezados
    ws.append(['Fecha', 'Mascota', 'Especie', 'Cliente', 'Motivo', 'Diagnóstico', 'Tratamiento'])

    for c in consultas:
        ws.append([
            c.fecha.strftime('%Y-%m-%d'),
            c.mascota.nombre,
            c.mascota.especie,
            c.mascota.cliente.nombre,
            c.motivo,
            c.diagnostico or '',
            c.tratamiento or '',
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=consultas.xlsx'
    wb.save(response)
    return response
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def generar_boleta_pdf(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    template_path = 'gestion/boleta_pdf.html'
    context = {'consulta': consulta}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="boleta_{consulta.id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa.CreatePDF(html, dest=response)
    return response
def historial_mascota_pdf(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    consultas = Consulta.objects.filter(mascota=mascota).order_by('fecha')

    template_path = 'gestion/historial_pdf.html'
    context = {
        'mascota': mascota,
        'consultas': consultas,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=historial_{mascota.nombre}.pdf'
    # Para xhtml2pdf, aseguramos que los archivos estáticos sean accesibles
    from django.conf import settings
    from django.templatetags.static import static
    import os
    # Pasar la ruta absoluta del logo si se requiere
    context['logo_url'] = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo_unmsm.png')
    template = get_template(template_path)
    html = template.render(context)
    pisa.CreatePDF(html, dest=response, encoding='utf-8')
    return response
