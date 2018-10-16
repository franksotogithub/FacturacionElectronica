
$utils.locales.datatable = undefined;

$utils.locales.crearDataTablaLocales=function(tabla,data){

        if(!($utils.locales.datatable===undefined)){
            $utils.locales.datatable.destroy();
        }


        var columns = [
                    {data: 'codigo' ,'searchable':false},
                    {data: 'tipo' ,'searchable':false},
                    {data: 'domicilio' ,'searchable':true},
                    {data: 'codigo_original' ,'searchable':true},
                    {data: 'id'  ,'searchable':true},
        ];

        $utils.locales.datatable= tabla.DataTable({
            data:data,
            columns:columns,
            "columnDefs": [
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
            scrollY: "500px",
            autoWidth: true,
            ordering: false,
            searching: false,
            fixedRowHeight:false,
            scrollX: false,


        });
}


$utils.locales.TablaLocales = function(){
    var tabla=$('#tabla_locales');
    $services.configuracion.listarLocales(function (data) {

        $utils.locales.crearDataTablaLocales(tabla,data);
    });
}


$utils.locales.detalleLocal = function(tipo,id){
    if (tipo==tipoAc.TIPO_ACTUALIZAR){

        $services.configuracion.getLocal(id ,function (data) {

            $('#codigo').val(data.codigo);
            $('#tipo').val(data.tipo);
            $('#domicilio').val(data.domicilio);
            $('#codigo_original').val(data.codigo_original);

            $('#eliminar').css('display','inline');
        } );

    }

    else{
        $('#codigo').val('');
       $('#tipo').val('');
       $('#domicilio').val('');
       $('#codigo_original').val('');
        $('#eliminar').css('display','none');
    }

    $("#modal_detalle").modal('show');
}


$utils.locales.guardar=function(tipo,data,id){

     swal({
            title: "Guardar",
            text: "Desea Guardar los datos",
            type: "warning",
            showCancelButton: true,
            closeOnConfirm: true,
            confirmButtonColor: "#2196F3",
        },  function() {
             if(tipo==tipoAc.TIPO_ACTUALIZAR){
                $services.configuracion.actualizarLocal(data,id,function () {
                    swal('Local actualizado');
                    $("#modal_detalle").modal('hide');
                    $utils.locales.TablaLocales();
                });
            }
            else{
                $services.configuracion.crearLocal(data,function () {
                    swal('Local creado');
                    $("#modal_detalle").modal('hide');
                    $utils.locales.TablaLocales();
                });

             }


     });


}


$utils.locales.eliminar=function(id){
     swal({
            title: "Eliminar",
            text: "Deseas eliminar el local",
            type: "warning",
            showCancelButton: true,
            closeOnConfirm: true,
            confirmButtonColor: "#2196F3",
        },  function() {

                $services.configuracion.eliminarLocal(id,function () {
                    swal('Local eliminado');
                    $("#modal_detalle").modal('hide');
                    $utils.locales.TablaLocales();
                });
     });


}