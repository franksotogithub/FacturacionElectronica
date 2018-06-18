$services.facturacion.getFacturas= function (callbacksuccess) {
    var slug = 'facturacion/facturas/';
    $services.ajax.get({
        url: $utils.urlServer(slug),
        success: function (data) {

            callbacksuccess(data);
        },

        }
    );
}


