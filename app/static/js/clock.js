// import "bootswatch/dist/lux/bootstrap.min.css"

const oTime = document.getElementById("o-time");
const oDate = document.getElementById("o-date");
const cTime = document.getElementById("c-time");
const cDate = document.getElementById("c-date");

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

const interval = setInterval( () => {
  const local = new Date();
  
  let day = local.getDate(),
    month = local.getMonth(),
     year = local.getFullYear();

    oTime.innerHTML = local.toLocaleTimeString();
    oDate.innerHTML = `${day} ${monthNames[month]} ${year}`;
    cTime.innerHTML = local.toLocaleTimeString();
    cDate.innerHTML = `${day} ${monthNames[month]} ${year}`
}, 1000);
