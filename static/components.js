document.addEventListener("DOMContentLoaded", function () {
    fetch("static/navbar.html")
        .then(response => response.text())
        .then(data => {
            document.body.insertAdjacentHTML("afterbegin", data);
        })
        .catch(error => console.error("Erro ao carregar a Navbar:", error));
});
