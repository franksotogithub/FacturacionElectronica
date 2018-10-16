
$utils.herramientas_datos.procesos = {
    "insertar_datos":{tipo:"comprobantes"},
    "insertar_resumenes":{tipo:"resumenComprobantes"},
    "insertar_anulaciones":{tipo:"resumenAnulados"},
    "exportar_sunat":{tipo:"exportarSunat"},
    "actualizar_estados":{tipo:"actualizarEstados"},

}
$utils.herramientas_datos.datatable= undefined;

$utils.herramientas_datos.crearTablaProcesos = function (tabla,data) {

        if(!($utils.herramientas_datos.datatable===undefined)){
            $utils.herramientas_datos.datatable.destroy();
        }

        var columns = [
            {data: 'id' ,'searchable':false},
            {data: 'descripcion' ,'searchable':true},
            {data: 'fecha_ini' },
            {data: 'fecha_fin' },
            {data: 'estado' },
            {data: 'icono' },
        ];

        $utils.herramientas_datos.datatable= tabla.DataTable({
            data:data,
            columns:columns,

            "columnDefs": [
                    {
                        targets: [0],
                        "visible":true,
                        "render": function (data, type, row,meta) {
                            return "<input class='form' type='checkbox' id="+data+">";
                        }
                    },


                    {
                        targets: [1],
                        "visible":true,
                        "render": function (data, type, row,meta) {
                            var html ="<div>";
                            html +="<li class='"+row.icono+"' style='font-size: 20px'> ";
                            html +="<span>";
                            html +=data;
                            html +="</span>";
                            html +="</li>";
                            return html;
                        }
                    },


                    {
                        targets: [2,3],
                        "visible":true,
                        "render": function (data, type, row,meta) {
                            var html =$utils.blankTonull($utils.isoformatToDatetime(data));
                            return html;
                        }
                    },

                    {
                        targets: [-1],
                        "visible":false,
                    },
                ],
            createdRow: function (row, data, dataIndex) {
                  $(row).attr('id',data.id);
                },
            bLengthChange: false,
            bPaginate: true,
            bInfo: false,
            scrollY: "300px",
            autoWidth: true,
            ordering: false,
            searching: false,
            fixedRowHeight:false,
            scrollX: false,
        });

};

$utils.herramientas_datos.listarProcesos = function () {
    var tabla =$('#tabla_procesos');
    $services.herramientas.listarProcesos(function (data) {
        $utils.herramientas_datos.crearTablaProcesos(tabla,data)
    });
}

$utils.herramientas_datos.ejecutar = function (idAccion) {
    var datax;
    var tipo='';
    tipo=$utils.herramientas_datos.procesos[idAccion].tipo;
    datax={'tipo' : tipo,
           'csrfmiddlewaretoken' : App.csrf_token,};


    swal({
            title: "Ejecutar Proceso",
            text: "Ejecutar el proceso",
            type: "warning",
            showCancelButton: true,
            closeOnConfirm: false,
            //confirmButtonColor: "#2196F3",
            },
        function() {

            $services.comprobante.herramientasDatos(datax,
                function (data) {
                    if(data.status) {
                         swal({
                         title: "Proceso Finalizado!",
                         confirmButtonColor: "#2196F3"
                         });
                    }

                    else {
                        swal({
                         title: "No se ha culminado el proceso",
                         confirmButtonColor: "#2196F3"
                         });
                    }

                },
                function (data) {
                     swal({
                         title: "Error de Servicio",
                         confirmButtonColor: "#2196F3"
                         });
                }


            );

        });


    /*$('#'+idAccion).on('click', function() {

    });*/





}


$utils.herramientas_datos.ejecutarProcesos = function (listProcesos) {
    var datax;

    datax={'procesos' : listProcesos,
           'csrfmiddlewaretoken' : App.csrf_token,};


    swal({
            title: "Ejecutar Proceso",
            text: "Ejecutar el proceso",
            type: "warning",
            showCancelButton: true,
            closeOnConfirm: true,
            //confirmButtonColor: "#2196F3",
            //showLoaderOnConfirm: true
        },
        function() {
            $services.herramientas.ejecutarProcesos(datax,function (data) {
                if(data.success) {
                         swal({
                         title: "Ejecutando proceso!",
                         confirmButtonColor: "#2196F3"
                         });
                    }
                else {
                        swal({
                         title: "Error de ejecucion",
                         confirmButtonColor: "#2196F3"
                         });
                }

                },  function (data) {
                     swal({
                         title: "Error de Servicio",
                         confirmButtonColor: "#2196F3"
                         });
                }

                );
            $utils.herramientas_datos.listarProcesos();
        });


}


