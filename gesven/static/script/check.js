//  Style for Pin Validator
let confirmPin = document.querySelector('input[name="confirm-pin"]');

if (confirmPin != null) {
  confirmPin.addEventListener("keyup", validator);

  function validator(e) {
    let pin = document.querySelector('input[name="pin"]');
    let submitBtn = document.getElementById("submit-form");

    if (confirmPin.value === pin.value) {
      confirmPin.classList.replace("is-invalid", "is-valid");
      submitBtn.classList.remove("disabled");
    } else {
      confirmPin.classList.add("is-invalid");
      submitBtn.classList.add("disabled");
    }
  }
}

// Style and block for Pin Access Control
let controlPin = document.getElementById("PIN");
if (controlPin != null) {
  controlPin.addEventListener("keyup", () => {
    let expReg = /\D/;
    console.log(expReg.test(controlPin.value));
    if (expReg.test(controlPin.value)|| controlPin.value=='') {
      controlPin.classList.remove('is-valid');
      controlPin.classList.add('is-invalid');
    } else {
      controlPin.classList.remove('is-invalid');
      controlPin.classList.add('is-valid')
    }
  });
}
