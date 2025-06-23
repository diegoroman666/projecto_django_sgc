
from django.contrib import admin
from django.urls import path
from import_csv import views
from import_csv.views import importar_csv , mostrarListado, mostrar_listadoo, mostrarIndexCopy

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.mostrarIndexCopy ),
    path('index_copy',views.mostrarIndexCopy),
    path('index',views.mostrarIndexCopy),
    path('login', views.iniciarSesion),
    path('logout', views.cerrarSesion),


    path('menu_admin', views.mostrarMenuAdmin),
    path('form_registrar/', views.mostrarRegistro ),
    path('listado/', views.mostrarListado),
    path('form_registrar/insertar_correspondencia/', views.insertarCorrespondencias, name='insertar_correspondencia'),
    path('form_actualizar_correspondencia/<int:id>', views.mostrarFormActualizarCorrespondencia),
    path('actualizar_correspondencia/<int:id>', views.actualizarCorrespondencia),
    path('eliminar_correspondencia/<int:id>', views.eliminarCorrespondencia),
    path('listado/filtroContenga',views.filtroContenga),
    path('listar_historial', views.mostrarListarHistorial),
    path('acerca_de/', views.acerca_de, name='acerca_de'),
    

    path('importar_csv/', importar_csv, name='importar_csv'),
    path('listadoo/', mostrar_listadoo, name='mostrar_listado'),  # Nueva ruta

    path('menu_usuario', views.mostrarMenuUsuario),
    path('', views.mostrarIndex),
    path('form_registrar_copy/', views.mostrarRegistroCopy ),
    path('listado_copy/', views.mostrarListadoCopy),
    path('form_registrar_copy/insertar_correspondencia/', views.insertarCorrespondenciasCopy),
    path('eliminar_correspondencia_copy/<int:id>', views.eliminarCorrespondenciaCopy),
    path('listado_copy/filtroContenga',views.filtrooContenga),

    path('vaciar_tabla/', views.vaciar_tabla, name='vaciar_tabla'),
    path('listado_copy/', views.mostrarListadoCopy, name='listado_copy'),  # Ruta original del listado
    
    path('ver_estadisticas/', views.ver_estadisticas, name='ver_estadisticas'),
    path('grafico_circular/', views.grafico_circular, name='grafico_circular'),
    path('memoria/', views.memoria, name='memoria')


]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
