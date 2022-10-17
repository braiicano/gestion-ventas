//  Style for Pin Validator
let confirmPin = document.querySelector('input[name="confirm-pin"]');

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

// Style and block for Pin Access Control
let controlPin = document.getElementById('PIN');
controlPin.addEventListener("keyup",()=>{
  if (controlPin.value in  /([0-9]+)/){
    confirmPin.classList.replace('is-invalid','is-valid');
  }else{
    confirmPin.classList.add('is-invalid');
  }
})