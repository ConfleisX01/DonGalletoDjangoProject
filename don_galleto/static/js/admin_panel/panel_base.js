// Funciones para la administracion
// Seccion del CRUD de clientes

function confirmarAccion(url) {
    Swal.fire({
        title: '¿Quieres realizar esta acción?',
        icon: 'warning',
        showCancelButton: false,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url
        }
    })
}