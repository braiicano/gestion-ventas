function catchEnter(e) {
  let trigger = document.querySelectorAll('input[tag="trigger"]');
  let fieldsAreFill = false;
  let countNotFill = 0;

  for (let i = 0; i < trigger.length; i++) {
    const element = trigger[i];
    if (element.value == "") {
      countNotFill++;
    }
  }
  if (countNotFill === 0) fieldsAreFill = true;
  if (fieldsAreFill === false) {
    if (e.key == "Enter") {
      // alert("Los campos en rojo no pueden estar vacíos");
      e.preventDefault();
    }
  }
}
// Show datetime in document
function showDateTime(date, time) {
  const showTime = time
  const showDate = date
  const monthNames = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
  ];

  const interval = setInterval(() => {
    const local = new Date();

    let day = local.getDate(),
      month = local.getMonth(),
      year = local.getFullYear();

    showTime.innerHTML = local.toLocaleTimeString();
    showDate.innerHTML = `${day} ${monthNames[month]} ${year}`;
  }, 1000);
}

// Check password equals
function checkPass(e) {
  let item = e.currentTarget;
  let value = item.value;
  let confirmP;
  if (item.name.match("PASSWORD")) {
    confirmP = document.querySelector("input[tag='password']").value;
  } else if (item.name.match("PIN")) {
    confirmP = document.querySelector("input[tag='pin']").value;
  }
  let submitBtn = document.querySelector("[tag='submit']");
  if (value === confirmP) {
    item.classList.replace("is-invalid", "is-valid");
    submitBtn.classList.remove("disabled");
  } else {
    item.classList.add("is-invalid");
    submitBtn.classList.add("disabled");
  }
}

// Check Passwords values
function checkPasswordValue(e) {
  let item = e.currentTarget;
  let value = item.value;
  let insertIn = document.querySelector("[tag='passwordInsert']");
  let tagConfirm = document.querySelector("[tag='confirm']");
  let expNum = /[0-9]/;
  let expMay = /[A-Z]/;
  let expMin = /[a-z]/;
  let err = [];
  if (value.length < 8) {
    err.push("Debe ser mayor a 8 carácteres");
  }
  if (!expNum.test(value)) {
    err.push("Al menos un número");
  }
  if (!expMay.test(value)) {
    err.push("Al menos una mayúscula");
  }
  if (!expMin.test(value)) {
    err.push("Al menos una minúscula");
  }
  if (err.length > 0) {
    insertIn.innerHTML = err.toString();
    item.classList.remove("is-valid");
    item.classList.add("is-invalid");
  } else {
    insertIn.innerHTML = "";
    item.classList.remove("is-invalid");
    item.classList.add("is-valid");
  }
  if (value == tagConfirm.value) {
    tagConfirm.classList.remove("is-invalid");
    tagConfirm.classList.add("is-valid");
  } else {
    tagConfirm.classList.remove("is-valid");
    tagConfirm.classList.add("is-invalid");
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
// Verify only digits
function verifyInputCheck(e) {
  let item = e.currentTarget;
  let value = item.value;
  let expReg = /^[0-9]*[.]?[0-9]{0,2}$/;
  if (expReg.test(value)) {
    item.classList.remove("is-invalid");
    item.classList.add("is-valid");
  } else {
    if (e.key === "Enter") document.querySelector("form").preventDefault();
    item.classList.remove("is-valid");
    item.classList.add("is-invalid");
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
// Hidden and show values
function hidden(e) {
  let parent = e.currentTarget.parentNode;
  let show = parent.childNodes[3];
  if (show.toggleAttribute("type")) {
    show.setAttribute("type", "password");
  }
}
// Search elements
function searchElements(e) {
  let search = e.currentTarget;
  let container = document.querySelectorAll('[tag="searchParent"]');
  container.forEach((el) => {
    if (el.textContent.toLowerCase().includes(search.value.toLowerCase())) {
      el.style.display = "table-row";
    } else {
      el.style.display = "none";
    }
  });
}

//// Declarations
let d = document;
d.addEventListener("DOMContentLoaded", function () {
  if (d.URL.match("auth")) d.addEventListener("keyup", catchEnter);

  if (d.querySelector("input[tag='pin']")) {
    let items = d.querySelectorAll("input[tag='pin']");
    for (let item = 0; item < items.length; item++) {
      const element = items[item];
      element.addEventListener("keyup", verifyOnlyDigits);
    }
  }
  if (d.querySelector("input[tag='checker']")) {
    let items = d.querySelectorAll("input[tag='checker']");
    for (let item = 0; item < items.length; item++) {
      const element = items[item];
      element.addEventListener("keyup", verifyInputCheck);
    }
  }

  if (d.querySelector("input[tag='trigger']")) {
    let items = d.querySelectorAll("input[tag='trigger']");
    for (let item = 0; item < items.length; item++) {
      const element = items[item];
      element.addEventListener("keyup", verifyFillField);
    }
  }

  if (d.querySelector("input[tag='password']")) {
    d.querySelector("input[tag='password']").addEventListener(
      "keyup",
      checkPasswordValue
    );
  }

  if (d.querySelector("input[tag='confirm']")) {
    d.querySelector("input[tag='confirm']").addEventListener(
      "keyup",
      checkPass
    );
  }

  if (d.querySelector("div[tag='list_form']")) {
    let items = d.querySelectorAll("div[tag='list_form']");
    for (let item = 0; item < items.length; item++) {
      const element = items[item];
      let link = element.childNodes[1].childNodes[5];
      link.addEventListener("click", hidden);
    }
  }
  if (d.querySelector("input[tag='search']")) {
    d.querySelector("input[tag='search']").addEventListener(
      "keyup",
      searchElements
    );
  }
  if (d.querySelector("div[tag='showDateTime']")) {
    let listShowDateTime = d.querySelectorAll("div[tag='showDateTime']");
    listShowDateTime.forEach((e) => showDateTime(e.firstElementChild, e.lastElementChild));
  }
});
