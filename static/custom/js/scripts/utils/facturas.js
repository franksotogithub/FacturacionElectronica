$utils.facturas.datatable_contenido = undefined;
$utils.facturas.datatable_modal = undefined;

$utils.facturas.crearTablaFacturas= function (tabla,data){
    if (!($utils.facturas.datatable_contenido === undefined)) {
        $utils.facturas.datatable_contenido.destroy();
        }

        $utils.facturas.datatable_contenido = tabla.DataTable({
                "data": data,
                 columns: [
                    {data: 'idComprobante'},
                    {data: 'numDocUsuario'},
                    {data: 'rznSocialUsuario'},
                    {data: 'fecEmision'},
                    {data: 'mtoImpVenta'},
                    {data: 'numFactura'},
                ],

                "columnDefs": [
                    {
                        targets: -1,
                        "visible":true,
                        render: function (data,type,row) {
                            var html = '<input type="checkbox" class="" data-lote="'+data+'">';
                            return html;
                        },
                    },
                ],
                createdRow: function (row, data, dataIndex) {
                  $(row).attr('num-factura',data.numFactura);
                },

                bLengthChange: false,
                bPaginate: false,
                bInfo: false,
                scrollY: "500px",
                autoWidth: false,
                ordering: false,
                searching: false,
                fixedRowHeight:false,
                scrollX: false,
        });
}

$utils.facturas.listarFacturas = function(tabla){
    $services.facturacion.getFacturas(function (data) {
        $utils.facturas.crearTablaFacturas(tabla,data);
    });

}
