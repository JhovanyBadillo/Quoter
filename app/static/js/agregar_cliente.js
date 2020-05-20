let cp = document.getElementById('cp');
let rfc = document.getElementById('rfc');
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
        cp.setCustomValidity('Código Postal no válido. Debe componerse de 5 dígitos');
    } else {
        cp.setCustomValidity('');
    }
}

function validateRFC() {
    if (!validRFC.test(rfc.value)) {
        rfc.setCustomValidity('RFC no válido. Debe contener 12 o 13 caracteres');
    } else {
        rfc.setCustomValidity('');
    }
}

rfc.addEventListener("keyup", forceInputUppercase, false);
document.getElementById('nombre_corto').addEventListener("keyup", forceInputUppercase, false);
document.getElementById('razon_social').addEventListener("keyup", forceInputUppercase, false);
rfc.onchange = validateRFC;
rfc.onkeyup = validateRFC;
cp.onchange = validateCP;
cp.onkeyup = validateCP;

