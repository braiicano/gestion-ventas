const modalClose = document.getElementById("modal-info-close");
if (modalClose != null) {
  modalClose.addEventListener("click", () => {
    document.getElementById("modal-info").remove();
    document.getElementById("modal-js").remove();
  });
} else {
  document.getElementById("modal-js").remove();
}
