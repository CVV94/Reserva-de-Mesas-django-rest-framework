$(document).ready(function() {
    let dataTable;
    let dataTableIsInitialized = false;

    const initDataTable = async () => {
        if (dataTableIsInitialized) {
            dataTable.destroy();
        }
        dataTable = $('#datatable-products').DataTable({
            // Configuración en español
            language: {
                "lengthMenu":"Cantidad de Items _MENU_ por Página",
              "search": "Buscar:",
              "info":"Pagina _START_ - _END_ de _TOTAL_ entradas",
              "infoEmpty": "Mostrando 0 to 0 de 0 entradas",
              "paginate": {
                "last": "Ultima pagina",
                "previous": "Anterior",
                "next": "Siguiente",
            }

        }});
        dataTableIsInitialized = true;
    };

    window.addEventListener('load', async () => {
        await initDataTable();
    });
});