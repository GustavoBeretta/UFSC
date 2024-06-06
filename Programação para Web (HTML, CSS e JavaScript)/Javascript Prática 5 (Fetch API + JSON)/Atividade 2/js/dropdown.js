//Quando o usuário clica no botão, usa o toggle para alternar entre mostrar ou não 
//o conteúdo
function mostrarMenu(menuId) {
  //https://javascript.info/bubbling-and-capturing
  event.stopPropagation();
  document.getElementById(menuId).classList.toggle("show");
}
  
// Fecha o menu quando o usuário clica fora dee
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}