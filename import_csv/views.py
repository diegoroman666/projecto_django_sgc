import csv
from django.shortcuts import render
from django.http import HttpResponse
from import_csv.models import Correspondencia, Usuario , Historial
from .models import Correspondencia
from datetime import datetime

def mostrarIndexCopy(request):
    return render(request, 'index_copy.html')

def mostrarIndex(request):
    return render(request, 'index.html')

def iniciarSesion(request):
    if request.method == "POST":
        nom = request.POST["txtusu"]
        pas = request.POST["txtpas"]
        comprobarLogin = Usuario.objects.filter(nombre_usuario=nom, password_usuario=pas).values()

        if comprobarLogin:

            print(comprobarLogin[0])
            request.session["estadoSesion"] = True
            request.session["idUsuario"] = comprobarLogin[0]['id']
            request.session["nomUsuario"] = nom.upper()

            datos = { 'nomUsuario' : nom.upper() }


            # Se registra en la tabla historial.
            descripcion = "Inicia Sesión"
            tabla = ""
            fechayhora = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
            his.save()


            if nom.upper() == "ADMIN":
                return render(request, 'menu_admin.html', datos)
            else:
                return render(request, 'menu_usuario.html', datos)
        
        else:
            datos = { 'r2' : 'Error De Usuario y/o Contraseña!!' }
            return render(request, 'index_copy.html', datos)
    else:
        datos = { 'r2' : 'No Se Puede Procesar La Solicitud!!' }
        return render(request, 'index_copy.html', datos)

def cerrarSesion(request):
    try:

        # Se registra en la tabla historial.
        descripcion = "Cierra Sesión"
        tabla = ""
        fechayhora = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
        his.save()

        del request.session["estadoSesion"]
        del request.session["idUsuario"]
        del request.session["nomUsuario"]

        return render(request, 'index.html')
    except:
        return render(request, 'index.html')

def mostrarMenuAdmin(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() == "ADMIN":
            datos = { 'nomUsuario' : nomUsuario }
            return render(request, 'menu_admin.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

def mostrarMenuUsuario(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper() != "ADMIN":
            datos = { 'nomUsuario' : nomUsuario }
            return render(request, 'menu_usuario.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)

def mostrarIndex(request):
    return render(request, 'index.html')

def mostrarRegistroCopy(request):
    return render(request, 'form_registrar_copy.html')

def mostrarRegistro(request):
    return render(request, 'form_registrar.html')

def mostrarFormActualizarCorrespondencia(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["nomUsuario"] == "ADMIN":
                encontrado = Correspondencia.objects.get(id=id)
                opcionesCorrespondencia = Correspondencia.objects.all().values().order_by("folio")
                datos = { 
                    'nomUsuario' : request.session["nomUsuario"],
                    'encontrado' : encontrado,
                    'opcionesCorrespondencia' : opcionesCorrespondencia
                }
                return render(request, 'form_actualizar_correspondencia.html', datos)

            else:
                datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
                return render(request, 'index.html', datos)

        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)

    except:
        cor = Correspondencia.objects.select_related("correspondencia").all().order_by("folio")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'cor' : cor,
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Mostrar Datos!!'
        }

        return render(request, 'listado.html', datos)
    
def actualizarCorrespondencia(request, id):
    try:
        if request.method == "POST":
            folio = request.POST["txtfolio"].upper()
            fecha = request.POST["txtfecha"].upper()
            fechadocumento = request.POST["txtfechadocumento"].upper()
            foliooficina = request.POST["txtfoliooficina"].upper()
            tipodocumento = request.POST["txttipodocumento"].upper()
            remitente = request.POST["txtremitente"].upper()
            detalle = request.POST["txtdetalle"].upper()
            destino = request.POST["txtdestino"].upper()
            resolucion= request.POST["txtresolucion"].upper()
            fechadesapacho = request.POST["txtfechadespacho"].upper()
            

            cor = Correspondencia.objects.get(id=id)
            cor.folio = folio
            cor.fecha = fecha
            cor.fechadocumento = fechadocumento
            cor.foliooficina = foliooficina
            cor.tipodocumento = tipodocumento
            cor.remitente = remitente
            cor.detalle = detalle
            cor.destino = destino
            cor.resolucion = resolucion
            cor.fechadespacho = fechadesapacho
            cor.save()

            # Se registra en la tabla historial.
            descripcion = "Actualización realizada ("+str(folio.lower())+")"
            tabla = "Correspondencia"
            fechayhora = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(descripcion_historial=descripcion, tabla_afectada_historial=tabla, fecha_hora_historial=fechayhora, usuario_id=usuario)
            his.save()

            cor = Correspondencia.objects.select_related("correspondencia").all().values().order_by("folio")
            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'cor' : cor,
                'r' : 'Datos De La Correspondencia ('+str(folio)+') Modificados Correctamente!!'
            }
            return render(request, 'listado.html', datos)

        else:
            cor = Correspondencia.objects.select_related("correspondencia").all().order_by("folio")
            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'cor' : cor,
                'r2' : 'El ID ('+str(id)+') No Existe. Imposible Mostrar Datos!!'
            }
            return render(request, 'listado.html', datos)

    except:
        cor= Correspondencia.objects.select_related("correspondencia").all().order_by("folio")
        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'cor' : cor,
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar!!'
        }
        return render(request, 'listado.html', datos)  

def insertarCorrespondencias(request):
    fol = request.POST['txtfolio']
    fec= request.POST['txtfecha']
    fedoc = request.POST['txtfechadocumento']
    folioo = request.POST['txtfoliooficina']
    tipodoc= request.POST['txttipodocumento']
    rem = request.POST['txtremitente']
    det = request.POST['txtdetalle']
    des = request.POST['txtdestino']
    res= request.POST['txtresolucion']
    fedes = request.POST['txtfechadespacho']
    
    cor = Correspondencia(folio = fol , fecha = fec , fechadocumento = fedoc ,
                 foliooficina = folioo , tipodocumento = tipodoc , remitente = rem ,
                 detalle = det , destino = des , resolucion = res , fechadespacho = fedes )
    cor.save() #almacena en la BD la nueva correspondencia
    
    datos = {'r':'Correspondencia registrada correctamente!'}
    return render(request, 'form_registrar.html', datos)

def insertarCorrespondenciasCopy(request):
    fol = request.POST['txtfolio']
    fec= request.POST['txtfecha']
    fedoc = request.POST['txtfechadocumento']
    folioo = request.POST['txtfoliooficina']
    tipodoc= request.POST['txttipodocumento']
    rem = request.POST['txtremitente']
    det = request.POST['txtdetalle']
    des = request.POST['txtdestino']
    res= request.POST['txtresolucion']
    fedes = request.POST['txtfechadespacho']
    
    cor = Correspondencia(folio = fol , fecha = fec , fechadocumento = fedoc ,
                 foliooficina = folioo , tipodocumento = tipodoc , remitente = rem ,
                 detalle = det , destino = des , resolucion = res , fechadespacho = fedes )
    cor.save() #almacena en la BD la nueva correspondencia
    
    datos = {'r':'Correspondencia registrada correctamente!'}
    return render(request, 'form_registrar_copy.html', datos)

def eliminarCorrespondencia(request, id):
    cor = Correspondencia.objects.get(id = id)
    cor.delete() #esta instrucción es para eliminar un registro de la BD
    
    cor = Correspondencia.objects.all().values()
    datos = {'cor':cor, 'r':'Registro eliminado correctamente!'}
    return render(request, 'listado.html', datos)

def eliminarCorrespondenciaCopy(request, id):
    cor = Correspondencia.objects.get(id = id)
    cor.delete() #esta instrucción es para eliminar un registro de la BD
    
    cor = Correspondencia.objects.all().values()
    datos = {'cor':cor, 'r':'Registro eliminado correctamente!'}
    return render(request, 'listado_copy.html', datos)

def filtroContenga(request):
    filtro = request.POST['txtfil']
    cor = Correspondencia.objects.filter(remitente__contains = filtro).values()
    datos = {'cor':cor}
    return render(request, 'listado.html', datos)

def filtrooContenga(request):
    filtro = request.POST['txtfil']
    cor = Correspondencia.objects.filter(remitente__contains = filtro).values()
    datos = {'cor':cor}
    return render(request, 'listado_copy.html', datos)
    
def mostrarListarHistorial(request):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["nomUsuario"].upper() == "ADMIN":
                his = Historial.objects.select_related("usuario").all().order_by("-fecha_hora_historial")
                datos = {
                    'nomUsuario' : request.session["nomUsuario"],
                    'his' : his
                }
                return render(request, 'listar_historial.html', datos)

            else:
                datos = { 'r2' : 'No Tiene Permisos Suficientes Para Acceder!!' }
                return render(request, 'index.html', datos)

        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)

    except:
        datos = { 'r2' : 'Error Al Obtener Historial!!' }
        return render(request, 'index.html', datos)

def importar_csv(request):
    if request.method == 'POST' and request.FILES['archivo_csv']:
        archivo_csv = request.FILES['archivo_csv']
        
        # Lee el archivo CSV
        reader = csv.reader(archivo_csv.read().decode('utf-8').splitlines())
        next(reader)  # Omite la cabecera
        
        # Importa los datos
        for row in reader:
            _, created = Correspondencia.objects.get_or_create(
                
                fecha=row[0],
                fechadocumento=row[1],
                folio=row[2],
                foliooficina=row[3],
                remitente=row[4],
                tipodocumento=row[5],
                detalle=row[6],
                destino=row[7],
                resolucion=row[8],
                fechadespacho=row[9]
            )
        
        return render(request, 'importacion_completa.html')  # Renderiza la nueva plantilla
    
    return render(request, 'importar_csv.html')


def mostrar_listadoo(request):
    correspondencias = Correspondencia.objects.all()  # Obtiene todos los registros
    return render(request, 'listado.html', {'correspondencias': correspondencias})

def mostrarListado(request):
    cor = Correspondencia.objects.all().values().order_by('id')
    datos = {'cor':cor}
    return render(request, 'listado.html', datos)

def mostrarListadoCopy(request):
    cor = Correspondencia.objects.all().values()
    datos = {'cor':cor}
    return render(request, 'listado_copy.html', datos)

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Correspondencia

from django.shortcuts import redirect, render
from .models import Correspondencia  # Asegúrate de usar tu modelo

def vaciar_tabla(request):
    # Elimina todos los registros de la tabla de correspondencias
    Correspondencia.objects.all().delete()
    # Redirige al HTML que muestra el mensaje de confirmación
    return render(request, 'vaciar_confirmacion.html')

def acerca_de(request):
    return render(request, 'acerca_de.html')

def memoria(request):
    return render(request, 'memoria.html')



#ESTADISTICAS

from django.shortcuts import render
from django.db.models import Count
import json
from .models import Correspondencia  # Importa tu modelo correspondiente


def ver_estadisticas(request):
    # Lista de atributos disponibles en la tabla Correspondencia
    atributos = ['fecha', 'fechadocumento', 'folio', 'foliooficina', 'remitente', 'tipodocumento', 'detalle', 'resolucion', 'fechadespacho']

    labels = []
    data = []
    eje_x_name = ''  # Guardar el nombre del atributo seleccionado

    if request.method == 'POST':
        eje_x = request.POST.get('eje_x')  # Variable seleccionada para el eje X

        if eje_x:
            # Guardar el nombre del atributo seleccionado
            eje_x_name = eje_x.capitalize()  # Capitalizamos el nombre del atributo seleccionado

            # Obtener datos agrupados en tiempo real por el atributo seleccionado para el eje X
            consulta = Correspondencia.objects.values(eje_x).annotate(total=Count(eje_x)).order_by(eje_x)
            labels = [str(item[eje_x]) for item in consulta]  # Etiquetas para el eje X
            data = [item['total'] for item in consulta]  # Datos para el eje Y (conteo de registros)

    # Convertir los datos a JSON para poder ser usados en el gráfico
    labels_json = json.dumps(labels)
    data_json = json.dumps(data)

    # Renderizar la plantilla con los datos
    return render(request, 'ver_estadisticas.html', {
        'atributos': atributos,
        'labels': labels_json,
        'data': data_json,
        'eje_x_name': eje_x_name,  # Pasar el nombre del atributo seleccionado
    })


#DISPERSION

from django.shortcuts import render
import json

# Simulando una base de datos o un conjunto de datos
atributos = ["Remitente", "Destinatario", "Fecha", "Asunto"]  # Lista de atributos disponibles

# Nueva función para manejar el gráfico de dispersión
from django.shortcuts import render
from .models import Correspondencia
from django.db.models import Count
import json

def ver_estadisticas(request):
    # Lista de atributos disponibles en la tabla Correspondencia
    atributos = ['fecha', 'fechadocumento', 'folio', 'foliooficina', 'remitente', 'tipodocumento', 'detalle', 'resolucion', 'fechadespacho']

    labels = []
    data = []
    eje_x_name = ''  # Guardar el nombre del atributo seleccionado

    if request.method == 'POST':
        eje_x = request.POST.get('eje_x')  # Variable seleccionada para el eje X

        if eje_x:
            # Guardar el nombre del atributo seleccionado
            eje_x_name = eje_x.capitalize()  # Capitalizamos el nombre del atributo seleccionado

            # Obtener datos agrupados en tiempo real por el atributo seleccionado para el eje X
            consulta = Correspondencia.objects.values(eje_x).annotate(total=Count(eje_x)).order_by(eje_x)
            labels = [str(item[eje_x]) for item in consulta]  # Etiquetas para el eje X
            data = [item['total'] for item in consulta]  # Datos para el eje Y (conteo de registros)

    # Convertir los datos a JSON para poder ser usados en el gráfico
    labels_json = json.dumps(labels)
    data_json = json.dumps(data)

    # Renderizar la plantilla con los datos
    return render(request, 'ver_estadisticas.html', {
        'atributos': atributos,
        'labels': labels_json,
        'data': data_json,
        'eje_x_name': eje_x_name,  # Pasar el nombre del atributo seleccionado
    })

from django.shortcuts import render
from .models import Correspondencia
from django.db.models import Count
import json

def grafico_circular(request):
    # Atributos posibles para el gráfico circular
    atributos = ['fecha', 'fechadocumento', 'folio', 'foliooficina', 'remitente', 'tipodocumento', 'detalle', 'resolucion', 'fechadespacho']  # Puedes añadir más si es necesario

    labels = []
    data = []
    total_registros = 0
    atributo_seleccionado = ''

    if request.method == 'POST':
        atributo = request.POST.get('atributo')  # Atributo seleccionado para el gráfico circular

        if atributo:
            atributo_seleccionado = atributo.capitalize()

            # Consulta agrupada por el atributo seleccionado
            consulta = Correspondencia.objects.values(atributo).annotate(total=Count(atributo)).order_by(atributo)

            # Calcular el total de registros
            total_registros = sum(item['total'] for item in consulta)

            labels = [str(item[atributo]) for item in consulta]  # Etiquetas (categorías)
            data = [item['total'] for item in consulta]  # Cantidad de cada categoría

    # Convertir a JSON para el frontend
    labels_json = json.dumps(labels)
    data_json = json.dumps(data)
    total_registros_json = json.dumps(total_registros)

    return render(request, 'grafico_circular.html', {
        'atributos': atributos,
        'labels': labels_json,
        'data': data_json,
        'total_registros': total_registros_json,
        'atributo_seleccionado': atributo_seleccionado,
    })



