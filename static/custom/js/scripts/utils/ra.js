$utils.ra.datatableContenido = undefined;
$utils.ra.datatable = undefined;
$utils.ra.datatableDetalle = undefined;
$utils.ra.cfnumser=undefined
$utils.ra.cfnumdoc=undefined
$utils.ra.tipodoc=undefined
$utils.ra.nomArchivo=undefined
$utils.ra.tipoResumen='RA';

$utils.ra.crearTablaComprobantes=function(tabla,op){
        var columns = [

                    {data: 'fecha_gen' ,'searahable':false},
                    {data:'numser_resumen' ,'searahable':true},
                    {data:'numdoc_resumen' ,'searahable':true},
                    {data: 'estado' ,'searahable':true},
                    {data: 'nro_reg' ,'searahable':true},
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
            'tipoResumen':$utils.ra.tipoResumen
        }

        if (!($utils.ra.datatableContenido === undefined))
        {$utils.ra.datatableContenido.destroy();}

        $utils.ra.datatableContenido = tabla.DataTable({

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



$utils.ra.crearTablaDetalleComprobante = function (tabla, data) {
        if (!($utils.ra.datatableDetalle === undefined)) {
        $utils.ra.datatableDetalle.destroy();
        }

        $utils.ra.datatableDetalle = tabla.DataTable({
                "data": data,
                 columns: [
                    {data: 'tipodoc' },
                    {data: 'numserie_item' },
                    {data: 'numdoc_item'  },
                    {data: 'motivo_baja' },


                ],
                bLengthChange: false,
                bPaginate: false,
                bInfo: false,
                scrollY: "300px",
                autoWidth: false,
                ordering: false,
                searching: false,
                scrollX: true,

        });
}





$utils.ra.crearDetalleComprobante = function (resumen, tabla) {

    /*var $row = $(cell).closest('tr');

    var numser=$row.attr('numser_resumen');
    var numdoc=$row.attr('numdoc_resumen');
    var tipoResumen=$utils.ra.tipoResumen;*/

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
        $utils.ra.nomArchivo=data.cabecera.nom_archivo;

        $utils.ra.crearTablaDetalleComprobante(tabla,data.detalle);

    });
    $('#modal_detalle_factura').modal("show");
}

/*
$utils.ra.descargarPdf = function () {

    var cfnumser=$utils.ra.cfnumser;
    var cfnumdoc=$utils.ra.cfnumdoc;
    var tipodoc =$utils.ra.tipodoc ;

    $services.comprobante.descargarPdf(cfnumser,cfnumdoc,tipodoc,function (error){

        if(error==true){
            swal('No se puede descargar el arahivo, es posible q no exista');
        }
    });
}
*/


$utils.ra.descargarXml = function () {


    $services.comprobante.descargarXml($utils.ra.nomArchivo,function (error){
        if(error==true){
            swal('No se puede descargar el archivo, es posible q no exista');
        }
    });
}

$utils.ra.crearcombo = function (select){
    var html='<option value="" selected>TODOS</option>';
    $services.comprobante.getEstadosDocumentos(function (data) {
        data.forEach(function (el) {
            html+='<option value="'+el.id+'">'+el.nombre+'</option>';
        })
        select.html(html);
    });
}


$utils.ra.generarResumen = function(resumen,row)
{
    var d=$utils.ra.datatableContenido.row(row).data();

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

            d.numdoc_resumen=datos.numdoc_resumen;
            d.estado=datos.estado;
            row.attr('numdoc_resumen',datos.numdoc_resumen);
            row.attr('estado_resumen_id',datos.estado_resumen_id);
            $utils.ra.datatableContenido.row(row).data(d).invalidate();
            swal('documento generado');
        }

        else{
            swal('Problemas al generar docucumento');
        }


    })

}