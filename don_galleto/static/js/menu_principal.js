document.addEventListener("DOMContentLoaded", function () {
    // Selecciona todos los elementos con la clase "nav-group"
    const dropdowns = document.querySelectorAll(".nav-item.nav-group");

    dropdowns.forEach((dropdown) => {
        dropdown.addEventListener("click", function () {
            // Cierra todos los demás dropdowns antes de abrir el actual
            dropdowns.forEach((item) => {
                if (item !== dropdown) {
                    item.classList.remove("show");
                }
            });

            // Alterna la clase "show" en el elemento clickeado
            this.classList.toggle("show");
        });
    });
});
