import  json
from facturacion.utils import generar_txt_comprobantes_electronicos ,genera_pdf_facturas_electronicas,generar_txt_resumenes,generar_txt_resumenes_anulaciones
from facturacion.models import ComprobanteCab ,ResumenCab
from sunat.models import Documento

def crear_txt_comprobantes():

    comprobantes=ComprobanteCab.objects.filter(estado_comprobante=ComprobanteCab.POR_GENERAR_DOCUMENTO,tipodoc_comprobante__codigo__in=('01','07','08') ).order_by('-cffecdoc')
    #print('comprobantes>>>',comprobantes)
    for com in comprobantes:
        #try:

            nom_archivo=generar_txt_comprobantes_electronicos(com.cfnumser, com.cfnumdoc, com.tipodoc_comprobante_id)
            com.nom_archivo =nom_archivo
            com.estado_comprobante_id=ComprobanteCab.DOCUMENTO_GENERADO
            com.save()
            print('comprobantes>>>', nom_archivo)
            try:
                doc_sunat = Documento.objects.get(nom_arch=nom_archivo)
                doc_sunat.ind_situ=ComprobanteCab.DOCUMENTO_GENERADO
                doc_sunat.save()
    
            except:
                continue
        #except:
            #continue


def run():
    crear_txt_comprobantes()
    generar_txt_resumenes(ResumenCab.RESUMEN_COMPROBANTE)
    generar_txt_resumenes(ResumenCab.RESUMEN_ANULACION)
    #generar_txt_resumenes_anulaciones()




