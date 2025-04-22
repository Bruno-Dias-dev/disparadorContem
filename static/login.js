document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
  
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
  
    const response = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    });
  
    const resultado = document.getElementById("resultado");
  
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("token", data.token);
      resultado.innerText = "Login bem-sucedido!";
      // redirecionar ou fazer algo após o login
    } else {
      resultado.innerText = "Erro no login. Verifique suas credenciais.";
    }
  });
  