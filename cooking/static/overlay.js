function loginOverlayOn() {
    signUpOverlayOff();
    document.getElementById("login-overlay").style.display = "flex";
}
  
function loginOverlayOff() {
    document.getElementById("login-form").reset();
    document.getElementById("login-overlay").style.display = "none";
}

function signUpOverlayOn() {
    loginOverlayOff();
    document.getElementById("signup-overlay").style.display = "flex";
}
  
function signUpOverlayOff() {
    document.getElementById("signup-form").reset();
    document.getElementById("signup-overlay").style.display = "none";
}