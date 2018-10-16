var App = App || {};

var $utils = {
    init: function (options) {
        var version = 0.2;
        if (!(options === undefined)) {
            if (!(options.utils === undefined)) {
                for (var i in options.utils) {
                    $utils[options.utils[i]] = $utils[options.utils[i]] || {};
                    var file = App.require.script + "utils/" + options.utils[i] + ".js";
                    document.write('<scr' + 'ipt type="text/javascript" src="' + file + '?v=' + version + '"></scr' + 'ipt>');
                }
            }
        }
        return $utils;
    },

    arrayUnique: function (arrayOriginal) {
        var arraySinDuplicados = [];
        $.each(arrayOriginal, function(i, el){
            if($.inArray(el, arraySinDuplicados) === -1) arraySinDuplicados.push(el);
        });
        return arraySinDuplicados;
    },

    now: function (format) {
        try {
            if (format === undefined) {
                format = "DD/MM/YYYY";
            }
        } catch (err) {
            format = "DD/MM/YYYY";
        }

        return moment().format(format);
    },

    isoformatToDatetime: function (date_iso) {
        if (date_iso !==null)
        return moment(date_iso).format("DD/MM/YYYY HH:mm:ss");
        else
        return date_iso;
    },

    isoformatToDate: function (date_iso) {
        return moment(date_iso).format("DD/MM/YYYY");
    },

    pickerToIso: function (picker) {
        var date = moment(picker, "DD/MM/YYYY");
        if (date.isValid()) {
            date = date.toISOString();
        } else {
            date = "";
        }

        return date;
    },

    dateFormat: function (picker, initial, out) {
        return moment(picker, initial).format(out);
    },

    numberorfalse: function (val) {
        var val=$.trim(val);
        if (val != "" && !isNaN(val)) {
            return val;
        }
        else {
            return false;
        }
    },

    storage: function (name) {
        var local_data = JSON.parse(localStorage.getItem(name));
        if (local_data === null) {
            local_data = {};
        }
        return local_data;
    },

    keyExist: function (key, array) {
        var keys = Object.keys(array);
        if (keys.indexOf(key) >= 0) {
            return true;
        } else {
            return false;
        }
    },

    jsonLen: function (dict) {
        return Object.keys(dict).length;
    },

    milesFormat: function (number) {
        /*
         var num = number;
         if(!isNaN(num)){
         num = num.toString().split("").reverse().join("").replace(/(?=\d*\.?)(\d{3})/g,"$1,");
         num = num.split("").reverse().join("").replace(/^[\.]/,"");
         entrada = num;
         }else{
         entrada =number;
         }
         return entrada;
         */
        return number.toLocaleString('en-US');
    },

    cleanform: function (form, campos) {
        if (campos === undefined) {
            campos = ['input', 'textarea', 'select'];
        }

        $.each(campos, function (i,v) {
            $(form).find(v).each(function (ii,vv) {
                $(vv).val("");
            });
        });
    },

    zfill: function (num, places, val) {
        var zero = places - num.toString().length + 1;
        if (val === undefined) {
            val = 0;
        }
        return Array(+(zero > 0 && zero)).join(val) + num;
    },

    JsonMerge: function (obj1, obj2) {
        var result = {};
            for(var key in obj1) result[key] = obj1[key];
            for(var key in obj2) result[key] = obj2[key];
            return result;
    },

    modal_alert: function (modal, type, message) {
        var body = $(modal).find('.modal-body');
        var alert = $(body).find('.modal-alert');
        if (type == ':clean') {
            $(alert).remove();
        }else {
            if ($(alert).length > 0) {
                $(alert).remove();
            }

            var html = '<div class="alert alert-'+type+' alert-styled-left alert-bordered modal-alert">'+
                    '<button type="button" class="close" data-dismiss="alert"><span>×</span><span class="sr-only">Close</span></button>'+
                    message+
                    '</div>';

            $(body).prepend(html);
        }
    },


    modal_loading: function (modal) {
        var body = $(modal).find('.modal-body');
        var html = '<div class="alert alert-'+type+' alert-styled-left alert-bordered modal-alert">'+
                    '<button type="button" class="close" data-dismiss="alert"><span>×</span><span class="sr-only">Close</span></button>'+
                    message+
                    '</div>';

        $(body).prepend(html);


    },

    toInt: function (value) {
        var entero = parseInt(value);
        if (isNaN(value) || isNaN(entero)) {
            return 0;
        }else {
            return entero;
        }
    },

    boolToNumber: function (valor) {
        if (valor) {
            return 1;
        }else {
            return 0;
        }
    },

    blankTonull: function (valor) {
        if (valor == null){
            return '';
        }else {
            return valor;
        }
    },

    urlServer: function (slug) {
        var url = App.require.server + slug;
        //var url = App.require.server + slug + '?user_id=' + App.session.user.usuario;
        return url;
    },


    format: function(formatted, arguments) {
        for (var i = 0; i < arguments.length; i++) {
            var regexp = new RegExp('\\{'+i+'\\}', 'gi');
            formatted = formatted.replace(regexp, arguments[i]);
        }
        return formatted;
    },

    responseError: function(obj, msgerr) {
        if (!(obj.responseJSON === undefined)) {
            if (!(obj.responseJSON.detail === undefined)) {
                return obj.responseJSON.detail;
            }else {
                return msgerr;
            }
        }else {
            return msgerr;
        }
    },


     modal_exito: function (texto){
        if (texto===undefined) texto="Cambios guardados!"
        swal(
            {text:texto}
           /* ,function (confirm) {
                if (confirm) {swal.close();}
            }*/

        );



        //swal.close();
        //return false;
        //swal.stop();
        //swal.stopLoading();

    },


    render_confirm_save: function(button){
            $(button).attr("value","GUARDADO")
            $(button).removeClass("bg-success-300")
            $(button).addClass("bg-success-500")
            $(button).html('<i class="icon-checkmark4">GUARDADO</i>');
    },

    get_key_columns: function (columns,data) {

        var keys_columns=[]
        var el=''
        $.each(columns, function( index, value ) {
        el=value[data];
        keys_columns.push(el);
        });
        return keys_columns;
    },

    tablaPaginada : function (tabla,columns,url,data){

    },




};

$utils.init(App.filerequired);