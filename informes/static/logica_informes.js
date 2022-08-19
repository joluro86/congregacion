$(document).ready(function () {
    $('#tabla_informes_grupo').DataTable();
});

function guardar_informe_grupo(){
    console.log("aqui")    
    $.fn.dataTable.ext.buttons.sendTable = {
        text: "Send Table to Server",
        action: function ( e, dt, button, config ) {
            var table = dt.rows().data().toArray();
            $.ajax({
                type: "POST",
                url: "/guardar_informe_grupo",
                data: {
                    table: JSON.stringify(table)
                },
                success: function () {
                    alert("llegué")
                }
            });
        }
    };
}


