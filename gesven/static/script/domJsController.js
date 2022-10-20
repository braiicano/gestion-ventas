// Check password equals
function checkPasswords(e){
    let item = e.currentTarget;
    let value = item.value
    let confirmP = document.getElementById('PASS').value
    let submitBtn = document.getElementById("submit-form");

    if (value === confirmP) {
      item.classList.replace("is-invalid", "is-valid");
      submitBtn.classList.remove("disabled");
    } else {
      item.classList.add("is-invalid");
      submitBtn.classList.add("disabled");
    }
}
// Verify only digits
function verifyOnlyDigits(e) {
  let item = e.currentTarget;
  let value = item.value;
  let expReg = /\D/;
  if (expReg.test(value) || value == "") {
    item.classList.remove("is-valid");
    item.classList.add("is-invalid");
  } else {
    item.classList.remove("is-invalid");
    item.classList.add("is-valid");
  }
}

// Verify fill fields
function verifyFillField(e) {
  let item = e.currentTarget;
  let value = item.value;
  if (value == "") {
    if (item.classList.value.includes("is-valid")) {
      item.classList.replace("is-valid", "is-invalid");
    } else {
      item.classList.add("is-invalid");
    }
  } else {
    if (item.classList.value.includes("is-invalid")) {
      item.classList.replace("is-invalid", "is-valid");
    } else {
      item.classList.add("is-valid");
    }
  }
}
let d = document

d.addEventListener("DOMContentLoaded", function () {
    if (d.getElementById("NAME")){
        d.getElementById("NAME").addEventListener("keyup", verifyFillField);
    }
    if (d.getElementById("SURNAME")){
        d.getElementById("SURNAME").addEventListener("keyup", verifyFillField);
    }
    if (d.getElementById("EMAIL")){
        d.getElementById("EMAIL").addEventListener("keyup", verifyFillField);
    }
    if (d.getElementById("PASS")){
        d.getElementById("PASS").addEventListener("keyup", verifyFillField);
    }
    if (d.getElementById("DU")){
        d.getElementById("DU").addEventListener("keyup", verifyFillField);
    }
    if (d.getElementById("PIN")){
        d.getElementById("PIN").addEventListener("keyup", verifyOnlyDigits);
    }
    if (d.getElementById("USERNAME")){
        d.getElementById("USERNAME").addEventListener("keyup", verifyFillField);
    }
    if (d.getElementById("CONFIRM")){
        d.getElementById("CONFIRM").addEventListener("keyup", checkPasswords);
    }
    // d.getElementById("PIN").addEventListener("keyup", verifyFillField);
    // function that check Mayus, Numbers and letters >8 in password
  });
