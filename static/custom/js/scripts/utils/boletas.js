$utils.boletas.datatableContenido = undefined;
$utils.boletas.datatable = undefined;
$utils.boletas.datatableDetalle = undefined;
$utils.boletas.cfnumser=undefined
$utils.boletas.cfnumdoc=undefined
$utils.boletas.tipodoc=undefined


$utils.boletas.crearTablaComprobantes=function(tabla){
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
        var estado=$('#estado option:selected').val();
        var fecha =$('#fecha').attr('valor');

        var data={
            'serie':serie,
            'numdoc':numdoc,
            'razonsocial':razonsocial,
            'tipodoc':'03',
            'estado':estado,
            'fecha':fecha
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

        $utils.boletas.crearTablaDetalleComprobante(tabla,data.detalle);

    });
    $('#modal_detalle_factura').modal("show");
}

$utils.boletas.descargarPdf = function () {

    var cfnumser=$utils.boletas.cfnumser;
    var cfnumdoc=$utils.boletas.cfnumdoc;
    var tipodoc =$utils.boletas.tipodoc ;

    $services.comprobante.descargarPdf(cfnumser,cfnumdoc,tipodoc,function (error){

        if(error==true){
            swal('No se puede descargar el archivo, es posible q no exista');
        }
    });
}

$utils.boletas.descargarXml = function () {
    var cfnumser=$utils.boletas.cfnumser;
    var cfnumdoc=$utils.boletas.cfnumdoc;
    var tipodoc =$utils.boletas.tipodoc ;

    $services.comprobante.descargarXml(cfnumser,cfnumdoc,tipodoc,function (error){
        if(error==true){
            swal('No se puede descargar el archivo, es posible q no exista');
        }
    });
}

