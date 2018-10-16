import  json
from facturacion.utils import generar_txt_comprobantes_electronicos ,genera_pdf_facturas_electronicas,generar_txt_resumenes,generar_txt_resumenes_anulaciones,crear_txt_comprobantes
from facturacion.models import ComprobanteCab ,ResumenCab
from sunat.models import Documento
from django.db.models import Q


def run():
    crear_txt_comprobantes()
    generar_txt_resumenes(ResumenCab.RESUMEN_COMPROBANTE)
    generar_txt_resumenes(ResumenCab.RESUMEN_ANULACION)
    #generar_txt_resumenes_anulaciones()




