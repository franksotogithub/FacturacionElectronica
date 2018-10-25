$utils.facturas.datatableContenido = undefined;
$utils.facturas.datatable = undefined;
$utils.facturas.datatableDetalle = undefined;
$utils.facturas.cfnumser=undefined
$utils.facturas.cfnumdoc=undefined
$utils.facturas.tipodoc=undefined
$utils.facturas.nomArchivo='';
$utils.facturas.TIPOCOMPROBANTE='01';


$utils.facturas.crearTablaComprobantes=function(tabla,fechaIni,fechaFin,estado){
        var columns = [
                    {data: 'cffecdoc' ,'searchable':false},
                    {data:'cfnumser' ,'searchable':true},
                    {data:'cfnumdoc' ,'searchable':true},
                    {data: 'cfnombre' ,'searchable':true},
                    {data: 'estado_comprobante' ,'searchable':true},

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
            'tipodoc':$utils.facturas.TIPOCOMPROBANTE,
            'estado':estado,
            'fechaIni':fechaIni,
            'fechaFin':fechaFin
        }

        if (!($utils.facturas.datatableContenido === undefined))
        {$utils.facturas.datatableContenido.destroy();}

        $utils.facturas.datatableContenido = tabla.DataTable({

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


$utils.facturas.crearTablaDetalleComprobante = function (tabla, data) {
        if (!($utils.facturas.datatableDetalle === undefined)) {
        $utils.facturas.datatableDetalle.destroy();
        }

        $utils.facturas.datatableDetalle = tabla.DataTable({
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





$utils.facturas.crearDetalleComprobante = function (cell, tabla) {

    var $row = $(cell).closest('tr');
    var cfnumser=$row.attr('cfnumser');
    var cfnumdoc=$row.attr('cfnumdoc');
    var tipodoc=$row.attr('tipodoc_comprobante');
    $utils.facturas.cfnumser = cfnumser;
    $utils.facturas.cfnumdoc = cfnumdoc;
    $utils.facturas.tipodoc  = tipodoc ;

    var datax={
    'cfnumser'            : cfnumser ,
    'cfnumdoc'            : cfnumdoc  ,
    'tipodoc_comprobante' : tipodoc,
    'csrfmiddlewaretoken' : App.csrf_token,
    }



    $services.comprobante.getComprobante(datax,function (data){

        $('#cffecdoc').val(data.cabecera.cffecdoc);
        $('#cfnumdoc').val(data.cabecera.cfnumdoc);
        $('#estado_comprobante').val(data.cabecera.estado_comprobante);
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
        $utils.facturas.nomArchivo=data.cabecera.nom_archivo;
        $utils.facturas.crearTablaDetalleComprobante(tabla,data.detalle);

    });
    $('#modal_detalle_factura').modal("show");
}


$utils.facturas.descargarPdf = function () {

    /*var cfnumser=$utils.facturas.cfnumser;
    var cfnumdoc=$utils.facturas.cfnumdoc;
    var tipodoc =$utils.facturas.tipodoc ;
*/
    $services.comprobante.descargarPdf($utils.facturas.nomArchivo,function (error){

        if(error==true){
            swal('No se puede descargar el archivo, es posible q no exista');
        }
    });
}



$utils.facturas.descargarXml = function () {
    /*var cfnumser=$utils.facturas.cfnumser;
    var cfnumdoc=$utils.facturas.cfnumdoc;
    var tipodoc =$utils.facturas.tipodoc ;
*/
    $services.comprobante.descargarXml($utils.facturas.nomArchivo,function (error){
        if(error==true){
            swal('No se puede descargar el archivo, es posible q no exista');
        }
    });
}

$utils.facturas.crearCombo = function (select){
    var html='<option value="" selected>TODOS</option>';
    $services.comprobante.getEstadosDocumentos(function (data) {
        data.forEach(function (el) {
            html+='<option value="'+el.id+'">'+el.nombre+'</option>';
        })
        select.html(html);
    });
}

