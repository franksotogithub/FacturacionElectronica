import  json
from facturacion.utils import unzip_rpta_xml, actualizar_estado_comprobantes,actualizar_estado_resumenes,generar_pdf
from facturacion.models import ComprobanteCab , ResumenCab ,ResumenDet
from sunat.models import Documento
import requests
import os ,zipfile


        #except:
        #    continue
        #data= json.dumps({"nomArch": nom_arch})
        #r= requests.post(URL_REQUEST_GENERAR_PDF,data=data,headers=HEADERS)


def run():
    actualizar_estado_comprobantes()
    actualizar_estado_resumenes()
    generar_pdf()
    unzip_rpta_xml()


