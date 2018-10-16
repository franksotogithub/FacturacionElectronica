$services.configuracion.listarLocales= function (callbacksuccess) {
    var slug = 'configuracion_api/locales/';
    $services.ajax.get({
        url: $utils.urlServer(slug),
        success: function (data) {
            callbacksuccess(data);
            },
        });
}

$services.configuracion.getLocal= function (id, callbacksuccess) {
    var slug = 'configuracion_api/locales/'+id;
    $services.ajax.get({
        url: $utils.urlServer(slug),
        success: function (data) {
            callbacksuccess(data);
            },
        });
}


$services.configuracion.crearLocal= function (data, callbacksuccess) {
    var slug = 'configuracion_api/locales/';
    $services.ajax.post({
        url: $utils.urlServer(slug),
        success: function (data) {
            callbacksuccess(data);
            },
        }, data);
}

$services.configuracion.actualizarLocal= function (data,id, callbacksuccess) {
    var slug = 'configuracion_api/locales/'+ id+'/'
    $services.ajax.put({
        url: $utils.urlServer(slug),
        success: function (data) {
            callbacksuccess(data);
            },
        }, data);
}

$services.configuracion.eliminarLocal= function (id, callbacksuccess) {
    var slug = 'configuracion_api/locales/'+ id+'/'
    $services.ajax.delete({
        url: $utils.urlServer(slug),
        success: function (data) {
            callbacksuccess(data);
            },
        });
}

$services.configuracion.actualizarParametros= function (data,id, callbacksuccess) {
    var slug = 'configuracion_api/parametros/'+ id+'/'
    $services.ajax.delete({
        url: $utils.urlServer(slug),
        success: function (data) {
            callbacksuccess(data);
            },
        });
}