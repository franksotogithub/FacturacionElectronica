from configuracion.models import PadronRuc

def importar_datos_txt(filename,separated):
    # Using the newer with construct to close the file automatically.
    #with open(filename) as f:
    data = open(filename,encoding="utf8")

    for n, line in enumerate(data, 1):
        row=line.rstrip().split(separated)


