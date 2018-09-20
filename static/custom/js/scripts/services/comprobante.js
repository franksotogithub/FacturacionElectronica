$services.comprobante.getComprobantes= function (callbacksuccess) {
    var slug = 'facturacion-api/comprobantes/';
    $services.ajax.get({
        url: $utils.urlServer(slug),
        success: function (data) {

            callbacksuccess(data);
        },

        }
    );
}

$services.comprobante.getEstadosDocumentos= function (callbacksuccess) {
    var slug = 'facturacion-api/estados/';
    $services.ajax.get({
        url: $utils.urlServer(slug),
        success: function (data) {

            callbacksuccess(data);
        },

        }
    );
}


$services.comprobante.getComprobante= function (datax, callbacksuccess) {
    var slug = 'facturacion-api/comprobantes/detalle/'
    $services.ajax.post({
        url: $utils.urlServer(slug),
        success: function (data) {
            callbacksuccess(data);
            },
        }, datax);
}


$services.comprobante.getResumen= function (datax, callbacksuccess) {
    var slug = 'facturacion-api/resumenes/detalle/'
    $services.ajax.post({
        url: $utils.urlServer(slug),
        success: function (data) {
            callbacksuccess(data);
            },
        }, datax);
}


$services.comprobante.descargarPdf= function (nomArchivo,callback) {
    var error=false;
    var slug = 'facturacion-api/descargas/descargar-pdf/'+nomArchivo+'/';
    $.ajax({
        type:"GET",
        url: $utils.urlServer(slug),
        dataType:"html",
        contentType : 'application/pdf',
        success: function (res){
            window.open($utils.urlServer(slug));
            callback(error);
            },
        error:function (e) {
            error=true;
            callback(error);
            }});
}


/*
$services.comprobante.descargarXml= function (cfnumser,cfnumdoc,tipodoc,callback) {
    var error=false;
    var slug = 'facturacion-api/descargas/descargar-xml/'+cfnumser+'/'+cfnumdoc+'/'+tipodoc+'/';
    $.ajax({
        type:"GET",
        url: $utils.urlServer(slug),
        dataType:"html",
        contentType : 'application/xml',
        success: function (res){
            window.open($utils.urlServer(slug));
            callback(error);
            },
        error:function (e) {
            error=true;
            callback(error);
            }});
}
*/
$services.comprobante.descargarXml= function (nomArchivo,callback) {
    var error=false;
    var slug = 'facturacion-api/descargas/descargar-xml/'+nomArchivo+'/';
    $.ajax({
        type:"GET",
        url: $utils.urlServer(slug),
        dataType:"html",
        contentType : 'application/xml',
        success: function (res){
            window.open($utils.urlServer(slug));
            callback(error);
            },
        error:function (e) {
            error=true;
            callback(error);
            }});
}

$services.comprobante.generarResumen= function (datax, callbacksuccess) {
    var slug = 'facturacion-api/resumenes/generar_resumen/'
    $services.ajax.post({
        url: $utils.urlServer(slug),
        success: function (data) {
            callbacksuccess(data);
            },


        }, datax);
}