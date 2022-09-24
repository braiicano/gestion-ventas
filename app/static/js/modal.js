let close = document.querySelectorAll(".close-modal-view")[0];
let open = document.querySelectorAll(".open-modal-view")[0];
let modal = document.querySelectorAll(".pop-view")[0];
//let modalC = document.querySelectorAll(".pop-view-close")[0];

open.addEventListener("click",function(e){
  e.preventDefault();
  modal.classList.toggle('pop-view-close');
});
close.addEventListener("click", function(e){
  modal.classList.toggle('pop-view-close');
})
