$services.herramientas.listarProcesos= function (callbacksuccess) {
    var slug = 'herramientas_api/procesos/';
    $services.ajax.get({
        url: $utils.urlServer(slug),
        success: function (data) {
            callbacksuccess(data);
            },
        });
}


$services.herramientas.getLocal= function (id, callbacksuccess) {
    var slug = 'herramientas_api/procesos/'+id;
    $services.ajax.get({
        url: $utils.urlServer(slug),
        success: function (data) {
            callbacksuccess(data);
            },
        });
}


$services.herramientas.herramientasDatos= function (datax, callbacksuccess,callbackerror) {
    var slug = 'facturacion-api/herramientas/datos/'
    $services.ajax.post({
        url: $utils.urlServer(slug),
        success: function (data) {
                callbacksuccess(data);
                },
        error: function (data) {
                callbackerror(data);
            },
        }, datax);
}



$services.herramientas.ejecutarProcesos= function (datax, callbacksuccess,callbackerror) {
    var slug = 'herramientas_api/procesos/ejecutar_proceso/'
    $services.ajax.post({
        url: $utils.urlServer(slug),
        success: function (data) {
                callbacksuccess(data);
                },
        error: function (data) {
                callbackerror(data);
            },
        }, datax);
}


