const modalClose = document.getElementById("modal-info-close");
modalClose.addEventListener("click", () => {
  document.getElementById("modal-info").remove();
  document.getElementById("modal-js").remove();
});
