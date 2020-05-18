let cp = document.getElementById('cp');
let rfc = document.getElementById('rfc');
let razon_social = document.getElementById('razon_social');
let validCP = /^\d{5}$/;
let validRFC = /^\w{12,13}$/;

function forceInputUppercase(e) {
    let start = e.target.selectionStart;
    let end = e.target.selectionEnd;
    e.target.value = e.target.value.toUpperCase();
    e.target.setSelectionRange(start, end);
}

function validateCP() {
    if (!validCP.test(cp.value)) {
        cp.setCustomValidity('Código Postal no válido. Debe contener solamente 5 dígitos');
    } else {
        cp.setCustomValidity('');
    }
}

function validateRFC() {
    if (!validRFC.test(rfc.value)) {
        rfc.setCustomValidity('RFC no válido. Debe contener 12 0 13 caracteres');
    } else {
        rfc.setCustomValidity('');
    }
}

rfc.addEventListener("keyup", forceInputUppercase, false);
document.getElementById('nombre_corto').addEventListener("keyup", forceInputUppercase, false);
rfc.onchange = validateRFC;
cp.onchange = validateCP;

