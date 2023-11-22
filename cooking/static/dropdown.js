/* Inspired by a W3 Schools Tutorial for a Dropdown Menu:
https://www.w3schools.com/howto/howto_js_dropdown.asp */

var shown = false;

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function dropdownFunc() {
    document.getElementById("user-dropdown").classList.toggle("show");
    shown = !shown;
}
  
// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbutton') && shown) {
    document.getElementById("user-dropdown").classList.toggle("show");
    shown = !shown;
  }
}