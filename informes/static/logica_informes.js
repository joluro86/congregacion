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


function on(checkbox) {
    id = checkbox.value;
    grupo = document.getElementById('grupo').value
    estado = '1'
    window.location.href = "/cambiar_estado_informe/" + id + "/" + grupo + "/" + estado + "/";
}

function off(checkbox) {
    id = checkbox.value;
    grupo = document.getElementById('grupo').value
    estado = '0'
    window.location.href = "/cambiar_estado_informe/" + id + "/" + grupo + "/" + estado + "/";
}

function funcion_cambio_estado(id) {
    estado = 'estado' + id;
    var checkbox = document.getElementById(estado);
    checkbox.addEventListener("change", comprueba, false);

    function comprueba() {
        if (checkbox.checked) {
            on(checkbox);
        } else {
            off(checkbox);
        }
    }
}
