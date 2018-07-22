$utils.consultar_comprobante.datatableContenido = undefined;
$utils.consultar_comprobante.datatable = undefined;
$utils.consultar_comprobante.datatableDetalle = undefined;
$utils.consultar_comprobante.cfnumser=undefined
$utils.consultar_comprobante.cfnumdoc=undefined
$utils.consultar_comprobante.tipodoc=undefined
$utils.consultar_comprobante.data=undefined


$utils.consultar_comprobante.crearTablaComprobante=function(tabla,data){

    if (!($utils.consultar_comprobante.datatableContenido === undefined)) {
        $utils.consultar_comprobante.datatableContenido.destroy();
        }
    $utils.consultar_comprobante.datatableContenido = tabla.DataTable({
        "data": data,
        columns: [
            {data: 'cffecdoc' },
            {data:'cfnumser' },
            {data:'cfnumdoc' },
            {data: 'cfnombre' },
            {data: 'importe_total_venta'},
            {data:'cfnumdoc' },
        ],
        "columnDefs": [
            {
                targets: -1,
                render: function (data, type, row) {
                    var html = '<button  class="btn btn-success bg-success-300 descargar_xml" >DESCARGAR XML</button>';
                    return html;
                    }}
            ],
        createdRow: function (row, data, dataIndex) {
            $(row).attr('cfnumser',data.cfnumser);
            $(row).attr('cfnumdoc',data.cfnumdoc);
            $(row).attr('tipodoc_comprobante',data.tipodoc_comprobante);
            },
        bLengthChange: false,
        bPaginate: true,
        bInfo: false,
        scrollY: "200px",
        autoWidth: true,
        ordering: true,
        searching: false,
        fixedRowHeight:false,
        scrollX: false,
        });
}

$utils.consultar_comprobante.listarComprobantes = function(tabla,datax){
    $services.comprobante.getComprobante(datax,function (data) {
        var cabecera=[]
        if (data.status!=false)
            cabecera=[data.cabecera]
        else {
            cabecera=[];
            swal('No existe comprobante!');
        }
        $utils.consultar_comprobante.crearTablaComprobante(tabla,cabecera);


    });
};

$utils.consultar_comprobante.descargarPdf = function (cell) {
    var $row = $(cell).closest('tr');
    var cfnumser=$row.attr('cfnumser');
    var cfnumdoc=$row.attr('cfnumdoc');
    var tipodoc=$row.attr('tipodoc_comprobante');


    $services.comprobante.descargarPdf(cfnumser,cfnumdoc,tipodoc,function (error){

        if(error==true){
            swal('No se puede descargar el archivo, es posible q no exista');
        }
    });
}

$utils.consultar_comprobante.descargarXml = function (cell) {
    var $row = $(cell).closest('tr');
    var cfnumser=$row.attr('cfnumser');
    var cfnumdoc=$row.attr('cfnumdoc');
    var tipodoc=$row.attr('tipodoc_comprobante');

    $services.comprobante.descargarXml(cfnumser,cfnumdoc,tipodoc,function (error){
        if(error==true){
            swal('No se puede descargar el archivo, es posible q no exista');
        }
    });
}


