async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const response = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
  });

  const data = await response.json();
  if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      alert("Login realizado com sucesso!");
  } else {
      alert("Falha no login!");
  }
}

async function acessarProtegido() {
  const token = localStorage.getItem("token");
  const response = await fetch("http://127.0.0.1:8000/protected", {
      headers: { "Authorization": `Bearer ${token}` }
  });

  const resultado = await response.json();
  document.getElementById("resultado").innerText = JSON.stringify(resultado);
}