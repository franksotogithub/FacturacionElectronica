$utils.boletas.datatableContenido = undefined;
$utils.boletas.datatable = undefined;
$utils.boletas.datatableDetalle = undefined;
$utils.boletas.cfnumser=undefined
$utils.boletas.cfnumdoc=undefined
$utils.boletas.tipodoc=undefined
$utils.boletas.nomArchivo='';
$utils.boletas.TIPOCOMPROBANTE='03';


$utils.boletas.crearTablaComprobantes=function(tabla,fechaIni,fechaFin,estado){
        var columns = [
                    {data: 'cffecdoc' ,'searchable':false},
                    {data:'cfnumser' ,'searchable':true},
                    {data:'cfnumdoc' ,'searchable':true},
                    {data: 'cfnombre' ,'searchable':true},
                    {data: 'estado_comprobante.nombre' ,'searchable':true},


        ];
        var slug = 'facturacion-api/comprobantes/listar';
        var serie=$('#serie').val();
        var numdoc=$('#numdoc').val();
        var razonsocial=$('#razonsocial').val();

        //var fecha =$('#fecha').attr('valor');
        var fechaIni =fechaIni;
        var fechaFin =fechaFin;
        var data={
            'serie':serie,
            'numdoc':numdoc,
            'razonsocial':razonsocial,
            'tipodoc':$utils.boletas.TIPOCOMPROBANTE,
            'estado':estado,
            'fechaIni':fechaIni,
            'fechaFin':fechaFin
        }

        if (!($utils.boletas.datatableContenido === undefined))
        {$utils.boletas.datatableContenido.destroy();}

        $utils.boletas.datatableContenido = tabla.DataTable({

            "processing": true,
            "serverSide": true,

            "ajax":{
                url: $utils.urlServer(slug),
                "data": data,


            },
            createdRow: function (row, data, dataIndex) {
                  $(row).attr('cfnumser',data.cfnumser);
                  $(row).attr('cfnumdoc',data.cfnumdoc);
                  $(row).attr('tipodoc_comprobante',data.tipodoc_comprobante);
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


$utils.boletas.crearTablaDetalleComprobante = function (tabla, data) {
        if (!($utils.boletas.datatableDetalle === undefined)) {
        $utils.boletas.datatableDetalle.destroy();
        }

        $utils.boletas.datatableDetalle = tabla.DataTable({
                "data": data,
                 columns: [

                    {data: 'orden_item' },
                    {data: 'cant_item' },
                    {data: 'um_item' },
                    {data: 'cod_item'  },
                    {data: 'nom_item'  },
                    {data: 'imp_vu_item' },
                    {data: 'imp_total_item' },

                ],

                bLengthChange: false,
                bPaginate: false,
                bInfo: false,
                scrollY: "100px",
                autoWidth: false,
                ordering: false,
                searching: false,
                scrollX: true,
        });
}





$utils.boletas.crearDetalleComprobante = function (cell, tabla) {

    var $row = $(cell).closest('tr');
    var cfnumser=$row.attr('cfnumser');
    var cfnumdoc=$row.attr('cfnumdoc');
    var tipodoc=$row.attr('tipodoc_comprobante');
    $utils.boletas.cfnumser = cfnumser;
    $utils.boletas.cfnumdoc = cfnumdoc;
    $utils.boletas.tipodoc  = tipodoc ;

    var datax={
    'cfnumser'            : cfnumser ,
    'cfnumdoc'            : cfnumdoc  ,
    'tipodoc_comprobante' : tipodoc,
    'csrfmiddlewaretoken' : App.csrf_token,
    }



    $services.comprobante.getComprobante(datax,function (data){

        $('#cffecdoc').val(data.cabecera.cffecdoc);
        $('#cfnumdoc').val(data.cabecera.cfnumdoc);
        $('#estado_comprobante').val(data.cabecera.estado_comprobante.nombre);
        $('#cfcodcli').val(data.cabecera.cfcodcli);
        $('#nro_doc_receptor').val(data.cabecera.nro_doc_receptor);
        $('#cfnombre').val(data.cabecera.cfnombre);
        $('#moneda').val(data.cabecera.moneda);

        $('#tvv_cod_ope_exoneradas').val(data.cabecera.tvv_imp_ope_exoneradas);
        $('#total').val(data.cabecera.tvv_imp_ope_gravadas);
        $('#tvv_imp_ope_gravadas').val(data.cabecera.tvv_imp_ope_gravadas);
        $('#tvv_imp_ope_inafectas').val(data.cabecera.tvv_imp_ope_inafectas);
        $('#sumatoria_igv').val(data.cabecera.sumatoria_igv);
        $('#sumatoria_isc').val(data.cabecera.sumatoria_isc);
        $('#importe_total_venta').val(data.cabecera.importe_total_venta);
        $utils.boletas.nomArchivo=data.cabecera.nom_archivo;
        $utils.boletas.crearTablaDetalleComprobante(tabla,data.detalle);
     if(estado_comprobante!=='03')
        {
            $("#descargar_pdf").prop('disabled',true);
            $("#enviar_correo").prop('disabled',true);
        }
        else
        {
            $("#descargar_pdf").prop('disabled',false);
            $("#enviar_correo").prop('disabled',false);
        }
    });
    $('#modal_detalle_factura').modal("show");
}


$utils.boletas.descargarPdf = function () {

    /*var cfnumser=$utils.boletas.cfnumser;
    var cfnumdoc=$utils.boletas.cfnumdoc;
    var tipodoc =$utils.boletas.tipodoc ;
*/
    $services.comprobante.descargarPdf($utils.boletas.nomArchivo,function (error){

        if(error==true){
            swal('No se puede descargar el archivo, es posible q no exista');
        }
    });
}



$utils.boletas.descargarXml = function () {
    /*var cfnumser=$utils.boletas.cfnumser;
    var cfnumdoc=$utils.boletas.cfnumdoc;
    var tipodoc =$utils.boletas.tipodoc ;
*/
    $services.comprobante.descargarXml($utils.boletas.nomArchivo,function (error){
        if(error==true){
            swal('No se puede descargar el archivo, es posible q no exista');
        }
    });
}

$utils.boletas.crearCombo = function (select){
    var html='<option value="" selected>TODOS</option>';
    $services.comprobante.getEstadosDocumentos(function (data) {
        data.forEach(function (el) {
            html+='<option value="'+el.id+'">'+el.nombre+'</option>';
        })
        select.html(html);
    });
}

