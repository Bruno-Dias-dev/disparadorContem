document.addEventListener("DOMContentLoaded", async function () {
  const API_URL = "http://127.0.0.1:8000";
  const listaAgendamentos = document.getElementById("listaAgendamentos");

  async function carregarAgendamentos() {
    try {
      const response = await fetch(`${API_URL}/api/agendamentos/`);
      const agendamentos = await response.json();

      if (agendamentos.length === 0) {
        listaAgendamentos.innerHTML = `<p class="text-muted">Nenhum agendamento cadastrado.</p>`;
        return;
      }

      listaAgendamentos.innerHTML = ""; // Limpa antes de renderizar

      agendamentos.forEach((agendamento) => {
        const card = document.createElement("div");
        card.className = "col-md-4 mb-3";

        card.innerHTML = `
                    <div class="card mb-3" style="border-color:orange">
                        <div class="card-body">
                            <h5 class="card-title">Grupo ${
                              agendamento.nome
                            } </h5>                            
                            <p class="text-muted">Disparo em: ${formatarData(
                              agendamento.horario_disparo
                            )}</p>
                          <button class="btn btn-danger btn-sm btn-excluir" data-id="${agendamento.id}">
                            <i class="bi bi-trash"></i> 
                          </button>
                        </div>
                    </div> 
                `;
        listaAgendamentos.appendChild(card);
      });
    } catch (error) {
      console.error("❌ Erro ao carregar agendamentos:", error);
      listaAgendamentos.innerHTML = `<p class="text-danger">Erro ao carregar agendamentos.</p>`;
    }
  }

  window.deletarAgendamento = async function (id) {
    if (!confirm("Tem certeza que deseja excluir este agendamento?")) return;

    try {
      const response = await fetch(`${API_URL}/agendamento/${id}`, {
        method: "DELETE",
      });

      const result = await response.json();
      alert(result.message || result.error);

      if (!result.error) carregarAgendamentos();
    } catch (error) {
      console.error("Erro ao excluir grupo:", error);
    }
  };

  listaAgendamentos.addEventListener("click", function (event) {
    if (event.target.closest(".btn-excluir")) {
      const id = event.target.closest(".btn-excluir").getAttribute("data-id");
      deletarAgendamento(id);
    }
  });

  // Formatar listas para exibição
  function formatarLista(valor) {
    return valor ? (Array.isArray(valor) ? valor.join(", ") : valor) : "Nenhum";
  }

  // Formatar data para exibição
  function formatarData(data) {
    if (!data) return "Desconhecido";

    return new Date(data).toLocaleString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });
  }

  carregarAgendamentos();
});
