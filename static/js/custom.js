
function validateForm() {
    var pass = document.forms["myForm"]["pass"].value;
    var cpas = document.forms["myForm"]["cpass"].value;

    if (pass != cpas) {
        alert("pass not matchout");
        return false;
    }

}
