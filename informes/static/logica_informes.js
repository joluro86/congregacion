$(document).ready(function () {
    $('#tabla_informes_grupo').DataTable();
});

function confirmar_informe(numero_grupo) {
    Swal.fire({
        title: '¿Esta seguro?',
        text: "No podrá revertir esta acción!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Guardar!',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "/finalizar_informe/" + numero_grupo + "/";
        }
    })
}


