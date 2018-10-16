from __future__ import absolute_import
from celery import shared_task
from facturacion.utils import migrar_resumenes_anulados , migrar_comprobantes ,\
    actualizar_estados ,migrar_resumenes_comprobantes ,exportar_sunat , actualizar_estado_tarea

@shared_task
def generar_tareas_task(ids):
    for id in ids:
        actualizar_estado_tarea(id,'PROCESANDO')
        #try:
        if id==1:
            migrar_comprobantes()
        elif id==2:
            migrar_resumenes_comprobantes()
        elif id ==3:
            migrar_resumenes_anulados()
        elif id ==4:
            exportar_sunat()
        elif id == 5:
            actualizar_estados()
        else:
            continue
            #actualizar_estado_tarea(id, 'TERMINADO')
        #except:
            #actualizar_estado_tarea(id, 'ERROR')

@shared_task
def migrar_comprobantes_task():
    actualizar_estado_tarea(1, 'PROCESANDO')
    try:
        migrar_comprobantes()
        actualizar_estado_tarea(1, 'TERMINADO')
    except:
        actualizar_estado_tarea(1, 'ERROR')

@shared_task
def migrar_resumenes_comprobantes_task():
    actualizar_estado_tarea(2, 'PROCESANDO')
    try:
        migrar_resumenes_comprobantes()
        actualizar_estado_tarea(2, 'TERMINADO')
    except:
        actualizar_estado_tarea(2, 'ERROR')

@shared_task
def migrar_resumenes_anulados_task():
    actualizar_estado_tarea(3, 'PROCESANDO')
    try:
        migrar_resumenes_anulados()
        actualizar_estado_tarea(3, 'TERMINADO')
    except:
        actualizar_estado_tarea(3, 'ERROR')

@shared_task
def exportar_sunat_task():
    actualizar_estado_tarea(4, 'PROCESANDO')
    try:
        exportar_sunat()
        actualizar_estado_tarea(4, 'TERMINADO')
    except:
        actualizar_estado_tarea(4, 'ERROR')

@shared_task
def actualizar_estados_task():
    actualizar_estado_tarea(5, 'PROCESANDO')
    try:
        actualizar_estados()
        actualizar_estado_tarea(5, 'TERMINADO')
    except:
        actualizar_estado_tarea(5, 'ERROR')()
