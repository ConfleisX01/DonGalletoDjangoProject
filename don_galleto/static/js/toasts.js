const toastTrigger = document.getElementById('liveToastBtn')
const toastLiveExample = document.getElementById('liveToast')
if (toastTrigger) {
  toastTrigger.addEventListener('click', () => {
    const toast = new coreui.Toast(toastLiveExample)
    toast.show()
  })
}

document.addEventListener("DOMContentLoaded", function () {
  var toastEl = document.getElementById("liveToast");
  var toast = new coreui.Toast(toastEl); // Inicializar CoreUI Toast
  toast.show();
});
