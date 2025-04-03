document.addEventListener("DOMContentLoaded", function () {
    const barraProgreso = document.getElementById("barra-progreso");
    if (barraProgreso) {
        const progreso = parseFloat(barraProgreso.getAttribute("data-progreso")) || 0;
        updateProgressBar(barraProgreso, progreso);
    }
});

function updateProgressBar(barraProgreso, progreso) {
    barraProgreso.style.width = `${progreso}%`;
    barraProgreso.textContent = `${progreso.toFixed(2)}%`;

    if (progreso >= 100) {
        barraProgreso.classList.add("bg-success");
    } else if (progreso >= 75) {
        barraProgreso.classList.add("bg-info");
    } else if (progreso >= 50) {
        barraProgreso.classList.add("bg-warning");
    } else {
        barraProgreso.classList.add("bg-danger");
    }
}