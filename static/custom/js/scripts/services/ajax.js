$services.ajax = function (type, object, datos) {
    var default_success = function (data) {
        console.log(data);
    };

    var default_error = function () {
        console.log("error al conectarse con el servidor");
    };

    if (object === undefined) {
        object = {
            success: default_success,
            error: default_error
        };
    }else{
        if(!$utils.keyExist('success', object)) {
            object.success = default_success;
        }

        if (!$utils.keyExist('error', object)) {
            object.error = default_error
        }
    }

    var default_options = {
        url: object.url,
        type: type,
        dataType: 'JSON',
        beforesend: function () {},
        success: function (data) {
            object.success(data);
        },
        error: function (obj, status, othobj) {
            object.error(obj, status, othobj);
        }
    };

    if (type=='POST' || type=='PUT') {
            default_options.data = JSON.stringify(datos);
            default_options.contentType = 'application/json; charset=utf-8';
            if (!(datos.csrfmiddlewaretoken === undefined)) {
                default_options.headers = {
                    "X-CSRFToken": datos.csrfmiddlewaretoken
                }
            }
    }

    $.ajax(default_options);
};

$services.ajax.get = function (object) {
    //generico loading
    $services.ajax('GET', object);
};


$services.ajax.post = function (object, datos) {
    //generico loading
    $services.ajax('POST', object, datos);
};

$services.ajax.put = function (object, datos) {
    //generico loading
    $services.ajax('PUT', object, datos);
};

$services.ajax.delete = function (object) {
    $services.ajax('DELETE', object);
};

$services.ajax.recursiveSave = function (url, todo, inicio, total, finaliza) {
    var item = inicio + 1 ;
    if (item <= total) {
        //recursivo
        var data = todo[inicio];
        console.log(data);
        $service.ajax.put({
            url: url + data.id + '/',
            success: function () {
                $service.ajax.recursiveSave(url , todo, item, total, finaliza);
            },
            error: function () {
                $service.ajax.recursiveSave(url, todo, item, total, finaliza);
            }
        }, data)

    }else{
        finaliza();
    }
};

