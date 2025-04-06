const tabButtons = document.querySelectorAll('.nav-link');
    const btnUsuario = document.getElementById('btnCrearUsuario');
    const btnCliente = document.getElementById('btnCrearCliente');

    function toggleBotones(tabId) {
        if (tabId === 'user-off') {
            btnUsuario.classList.add('d-none');
            btnCliente.classList.remove('d-none');
        } else {
            btnUsuario.classList.remove('d-none');
            btnCliente.classList.add('d-none');
        }
    }

    // Al hacer clic en las tabs
    tabButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const targetId = e.target.getAttribute('data-bs-target').substring(1); // Quita el #
            toggleBotones(targetId);
        });
    });

    // Activar botón correcto al cargar (por si viene con la tab 'Clientes' activa)
    document.addEventListener('DOMContentLoaded', () => {
        const activeTab = document.querySelector('.nav-link.active');
        if (activeTab) {
            const tabId = activeTab.getAttribute('data-bs-target').substring(1);
            toggleBotones(tabId);
        }
    });

    const addSearch = (inputId, tableId) => {
    document.getElementById(inputId).addEventListener('keyup', function() {
        const searchValue = this.value.toLowerCase();
        const rows = document.querySelectorAll(`#${tableId} tr`);
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length >= 3) {
                const firstName = cells[0].textContent.toLowerCase();
                const lastName = cells[1].textContent.toLowerCase();
                const email = cells[2].textContent.toLowerCase();

                const match = firstName.includes(searchValue) || 
                            lastName.includes(searchValue) || 
                            email.includes(searchValue);

                row.style.display = match ? '' : 'none';
            }
        });
    });
}

    addSearch('searchAdmin', 'adminTable');
    addSearch('searchUser', 'userTable');
    addSearch('searchUser_off', 'userOffTable');