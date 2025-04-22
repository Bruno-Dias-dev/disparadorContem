document.addEventListener("DOMContentLoaded", async function () {
  const API_URL = "http://127.0.0.1:8000";
  const listaMensagens = document.getElementById("listaMensagens");

  async function carregarMensagens() {
    try {
      const response = await fetch(`${API_URL}/mensagens`);
      const mensagens = await response.json();

      if (mensagens.length === 0) {
        listaMensagens.innerHTML = `<p class="text-muted">Nenhuma mensagem cadastrado.</p>`;
        return;
      }

      listaMensagens.innerHTML = ""; // Limpa antes de renderizar
      mensagens.forEach((mensagem) => {
        const trueFalse = mensagem.ativo ? "Ativo" : "Inativo";
        const badgeColor = mensagem.ativo ? "success" : "danger";

        // Criando a linha da tabela
        const row = document.createElement("tr");
        row.innerHTML = `
              <td>${mensagem.id}</td>
              <td>${mensagem.title}</td>
              <td><span class="badge bg-${badgeColor}">${trueFalse}</span></td>
              <td>
                  <a href="/mensagens/edit/${mensagem.id}" class="btn btn-primary btn-sm">
                      <i class="bi bi-pencil"></i> 
                  </a>
                  <button class="btn btn-danger btn-sm btn-excluir" data-id="${mensagem.id}">
                      <i class="bi bi-trash"></i> 
                  </button>
              </td>
          `;

        listaMensagens.appendChild(row);
      });
    } catch (error) {
      console.error("❌ Erro ao carregar mensagens:", error);
    }
  }

  window.deletarmensagem = async function (id) {
    if (!confirm("Tem certeza que deseja excluir este mensagem?")) return;

    try {
      const response = await fetch(`${API_URL}/mensagens/${id}`, {
        method: "DELETE",
      });

      const result = await response.json();
      alert(result.message || result.error);

      if (!result.error) carregarMensagens();
    } catch (error) {
      console.error("Erro ao excluir mensagem:", error);
    }
  };

  listaMensagens.addEventListener("click", function (event) {
    if (event.target.closest(".btn-excluir")) {
      const id = event.target.closest(".btn-excluir").getAttribute("data-id");
      deletarmensagem(id);
    }
  });

  carregarMensagens();
});
