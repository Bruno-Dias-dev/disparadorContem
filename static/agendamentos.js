document.addEventListener("DOMContentLoaded", async function () {
  console.log("✅ Carregando grupos...");

  const API_URL = "http://127.0.0.1:8000";
  const listaAgendamentos = document.getElementById("listaAgendamentos");

  async function carregarAgendamentos() {
    try {
      const response = await fetch(`${API_URL}/agendamentos`);
      const agendamentos = await response.json();

      if (agendamentos.length === 0) {
        listaAgendamentos.innerHTML = `<p class="text-muted">Nenhum grupo cadastrado.</p>`;
        return;
      }

      listaAgendamentos.innerHTML = ""; // Limpa antes de renderizar

      agendamentos.forEach((agendamento) => {
        const card = document.createElement("div");
        card.className = "col-md-4 mb-3";

        card.innerHTML = `
                    <div class="card border-primary mb-3">
                        <div class="card-body">
                            <h5 class="card-title">${formatarData(
                              agendamento.horario_disparo
      )}</h5>                            
                            <p class="text-muted">Criado em: ${formatarData(
                              agendamento.created
                            )}</p>
                            <button class="btn btn-danger btn-sm" onclick="alert('Deseja excluir o grupo?')"><i class="bi bi-trash"></i> Excluir</button>

                        </div>
                    </div>
                `;
        listaAgendamentos.appendChild(card);
      });
    } catch (error) {
      console.error("❌ Erro ao carregar grupos:", error);
    }
  }

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
        hour12: false
    });
  }

  carregarAgendamentos();
});
