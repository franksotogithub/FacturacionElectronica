import  json
from facturacion.utils import generar_txt_resumenes,generar_txt_resumenes_anulaciones,ResumenCab
from facturacion.models import ComprobanteCab


def run():
    generar_txt_resumenes(ResumenCab.RESUMEN_COMPROBANTE)
    generar_txt_resumenes(ResumenCab.RESUMEN_ANULACION)


