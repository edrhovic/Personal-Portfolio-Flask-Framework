function togglePassword() {
    var passwordField = document.getElementById("password");
    var eyeIcon = document.querySelector(".toggle-password");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        eyeIcon.src = "/static/images/eye-off.png";
    } else {
        passwordField.type = "password";
        eyeIcon.src = "/static/images/eye-on.png";
    }
}