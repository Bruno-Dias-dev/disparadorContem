document.addEventListener("DOMContentLoaded", async function () {
  console.log("✅ Carregando grupos...");

  const API_URL = "http://127.0.0.1:8000";
  const listaGrupos = document.getElementById("listaGrupos");

  async function carregarGrupos() {
    try {
      const response = await fetch(`${API_URL}/grupos`);
      const grupos = await response.json();

      if (grupos.length === 0) {
        listaGrupos.innerHTML = `<p class="text-muted">Nenhum grupo cadastrado.</p>`;
        return;
      }

      listaGrupos.innerHTML = ""; // Limpa antes de renderizar

      grupos.forEach((grupo) => {
        const card = document.createElement("div");
        card.className = "col-md-4 mb-3";
        const trueFalse = grupo.ativo ? "Ativo" : "Inativo";
        const badgeColor = grupo.ativo ? "success" : "danger";

        card.innerHTML = `
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">${
                              grupo.nome
                            }</h5>                            
                            <p class="text-muted">Criado em: ${formatarData(
                              grupo.created
                            )}</p>
                            <div class="justify-content-between">
                            <a href="/edit/${
                              grupo.id
                            }" class="btn btn-primary"><i class="bi bi-pencil"></i> Editar
                            </a>
                            <span class="badge text-bg-${badgeColor}">${trueFalse}</span>
                            </div>
                            
                        </div>
                    </div>
                `;
        listaGrupos.appendChild(card);
      });
    } catch (error) {
      console.error("❌ Erro ao carregar grupos:", error);
    }
  }
  // <button class="btn btn-danger btn-sm" onclick="deletarGrupo(${grupo.id})"><i class="bi bi-trash"></i> Excluir</button>

  // Formatar listas para exibição
  function formatarLista(valor) {
    return valor ? (Array.isArray(valor) ? valor.join(", ") : valor) : "Nenhum";
  }

  // Formatar data para exibição
  function formatarData(data) {
    return data ? new Date(data).toLocaleDateString("pt-BR") : "Desconhecido";
  }

  // Redirecionar para a página de edição
  function editarGrupo(id) {
    alert("edit");
    window.location.href = `edit.html?grupoId=${id}`;
  }

  // Excluir um grupo
  async function deletarGrupo(id) {
    if (!confirm("Tem certeza que deseja excluir este grupo?")) return;

    try {
      const response = await fetch(`${API_URL}/grupos/${id}`, {
        method: "DELETE",
      });

      const result = await response.json();
      alert(result.message || result.error);

      if (!result.error) carregarGrupos();
    } catch (error) {
      console.error("Erro ao excluir grupo:", error);
    }
  }

  carregarGrupos();
});
