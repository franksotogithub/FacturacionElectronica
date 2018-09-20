$utils.rc.datatableContenido = undefined;
$utils.rc.datatable = undefined;
$utils.rc.datatableDetalle = undefined;
$utils.rc.cfnumser=undefined
$utils.rc.cfnumdoc=undefined
$utils.rc.tipodoc=undefined
$utils.rc.nomArchivo=undefined
$utils.rc.tipoResumen='RC';

$utils.rc.crearTablaComprobantes=function(tabla,op){
        var columns = [

                    {data: 'fecha_gen' ,'searchable':false},
                    {data:'numser_resumen' ,'searchable':true},
                    {data:'numdoc_resumen' ,'searchable':true},
                    {data: 'estado' ,'searchable':true},
                    {data: 'nro_reg' ,'searchable':true},
                    {data: 'id' ,'visible':false},
                    {data: 'tipo_resumen' ,'visible':false},
                    {data: 'estado_resumen_id' ,'visible':false},
        ];

        var slug = 'facturacion-api/resumenes/listar';
        /*var nomDocResumen=$('#nomDocResumen').val();
        var estado=$('#estado option:selected').val();
        var fechaIni =fechaIni;
        var fechaFin =fechaFin;
*/

        var data={
            'nomdocResumen':op.nomDocResumen,
            'estado':op.estado,
            'fechaIni':op.fechaIni,
            'fechaFin':op.fechaFin,
            'tipoResumen':$utils.rc.tipoResumen
        }

        if (!($utils.rc.datatableContenido === undefined))
        {$utils.rc.datatableContenido.destroy();}

        $utils.rc.datatableContenido = tabla.DataTable({

            "processing": true,
            "serverSide": true,

            "ajax":{
                url: $utils.urlServer(slug),
                "data": data,
            },


            createdRow: function (row, data, dataIndex) {

                  $(row).attr('id',data.id);
                  $(row).attr('numser_resumen',data.numser_resumen);
                  $(row).attr('numdoc_resumen',data.numdoc_resumen);
                  $(row).attr('tipo_resumen',data.tipo_resumen);
                  $(row).attr('estado_resumen_id',data.estado_resumen_id);
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
                bInfo: true,
                iDisplayLength: 10,
                columns:columns,
        });

    }



$utils.rc.crearTablaDetalleComprobante = function (tabla, data) {
        if (!($utils.rc.datatableDetalle === undefined)) {
        $utils.rc.datatableDetalle.destroy();
        }

        $utils.rc.datatableDetalle = tabla.DataTable({
                "data": data,
                 columns: [
                    {data: 'tipodoc' },
                    {data: 'numserie_item' },
                    {data: 'numdoc_item'  },
                    {data: 'tipdoc_identidad' },
                    {data: 'nrodoc_receptor' },
                    {data: 'importe_total_venta'  },
                    {data: 'estado'},

                ],
                bLengthChange: false,
                bPaginate: false,
                bInfo: false,
                scrollY: "300px",
                autoWidth: true,
                ordering: false,
                searching: false,
                scrollX: true,
        });
}





$utils.rc.crearDetalleComprobante = function (resumen, tabla) {

    //var $row = $(cell).closest('tr');
    //$utils.rc.cfnumser=$row.attr('numser_resumen');
    //$utils.rc.numdoc=$row.attr('numdoc_resumen');
    //$utils.rc.tipoResumen=$row.attr('tipoResumen');
    /*var numser=
    var numdoc=
    var tipoResumen=$utils.rc.tipoResumen;
*/
    var datax={
    'numser'  :  resumen.numser ,
    'numdoc'  :  resumen.numdoc  ,
    'tipoResumen' : resumen.tipoResumen,
    'csrfmiddlewaretoken' : App.csrf_token,
    }

    $services.comprobante.getResumen(datax,function (data){
        $('#cffecdoc').val(data.cabecera.fecha_gen);
        $('#cfnumdoc').val(data.cabecera.numser_resumen + '-'+data.cabecera.numdoc_resumen );
        $('#estado_resumen').val(data.cabecera.estado);
        $utils.rc.nomArchivo=data.cabecera.nom_archivo;
        $utils.rc.crearTablaDetalleComprobante(tabla,data.detalle);

    });
    $('#modal_detalle_factura').modal("show");
}

/*
$utils.rc.descargarPdf = function () {

    var cfnumser=$utils.rc.cfnumser;
    var cfnumdoc=$utils.rc.cfnumdoc;
    var tipodoc =$utils.rc.tipodoc ;

    $services.comprobante.descargarPdf(cfnumser,cfnumdoc,tipodoc,function (error){

        if(error==true){
            swal('No se puede descargar el archivo, es posible q no exista');
        }
    });
}
*/


$utils.rc.descargarXml = function () {
    $services.comprobante.descargarXml($utils.rc.nomArchivo,function (error){
        if(error==true){
            swal('No se puede descargar el archivo, es posible q no exista');
        }
    });
}



$utils.rc.crearCombo = function (select){
    var html='<option value="" selected>TODOS</option>';
    $services.comprobante.getEstadosDocumentos(function (data) {
        data.forEach(function (el) {
            html+='<option value="'+el.id+'">'+el.nombre+'</option>';
        })
        select.html(html);
    });
}


$utils.rc.generarResumen = function(resumen,row)
{
    var d=$utils.rc.datatableContenido.row(row).data();

    var datax={
    'numser'  : resumen.numser ,
    'numdoc'  : resumen.numdoc  ,
    'tipoResumen' : resumen.tipoResumen,
    'csrfmiddlewaretoken' : App.csrf_token,
    }

    $services.comprobante.generarResumen(datax,function (data) {
        if (data.success)
        {
            var datos=data.data;

            console.log('datos>>>',datos);
            d.numdoc_resumen=datos.numdoc_resumen;
            d.estado=datos.estado;
            row.attr('numdoc_resumen',datos.numdoc_resumen);
            row.attr('estado_resumen_id',datos.estado_resumen_id);
            $utils.rc.datatableContenido.row(row).data(d).invalidate();
            swal('documento generado');
        }

        else{
            swal('Problemas al generar docucumento');
        }


    })

}