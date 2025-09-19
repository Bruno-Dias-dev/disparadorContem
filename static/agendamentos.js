document.addEventListener("DOMContentLoaded", async function () {
  const API_URL = "http://212.85.21.32:8000";
  const apiUrl = API_URL;
  const listaAgendamentos = document.getElementById("listaAgendamentos");

  async function carregarAgendamentos() {
    try {
      const response = await fetch(`${apiUrl}/api/agendamentos/`);
      const agendamentos = await response.json();

      if (agendamentos.length === 0) {
        listaAgendamentos.innerHTML = `<p class="text-muted">Nenhum agendamento cadastrado.</p>`;
        return;
      }

      listaAgendamentos.innerHTML = ""; // Limpa antes de renderizar

      agendamentos.forEach((agendamento) => {
        const card = document.createElement("div");
        card.className = "col-md-4 mb-3";

        const horarioDisparo = new Date(agendamento.horario_disparo);
        const agora = new Date();
        const statusBadge =
          horarioDisparo < agora
            ? `<span class="badge bg-success">Enviados</span>`
            : `<span class="badge bg-warning text-dark">Agendado</span>`;
        console.log(
          `Agendamento: ${agendamento.nome}, Status: ${statusBadge}`
        );
        card.innerHTML = `
                    <div class="card mb-3" style="border-color:orange">
                        <div class="card-body">
                            <h5 class="card-title">Grupo ${
                              agendamento.nome
                            } </h5>                            
                            <p class="text-muted">Disparo em: ${formatarData(
                              agendamento.horario_disparo
                            )} - ${statusBadge}</p>
                             
                          <button class="btn btn-danger btn-sm btn-excluir" data-id="${
                            agendamento.id
                          }">
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

  window.deletarAgendamento = function (id) {
    Swal.fire({
      title: "Você tem certeza?",
      text: "Deseja excluir este agendamento?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Sim, excluir",
      cancelButtonText: "Cancelar",
      customClass: {
        confirmButton: "btn bg-prim",
        cancelButton: "btn btn-secondary",
      },
      buttonsStyling: false,
    }).then((result) => {
      if (result.isConfirmed) {
        excluirAgendamento(id);
      }
    });
  };

  async function excluirAgendamento(id) {
    try {
      const response = await fetch(`${apiUrl}/api/agendamento/${id}`, {
        method: "DELETE",
        credentials: "include",
      });

      const result = await response.json();

      await Swal.fire({
        icon: "success",
        title: "Sucesso!",
        text: result.message || "Agendamento excluído com sucesso.",
        confirmButtonText: "OK",
        customClass: {
          confirmButton: "btn bg-prim",
        },
        buttonsStyling: false,
      });

      window.location.href = "/agendamentos/";
    } catch (error) {
      await Swal.fire({
        icon: "error",
        title: "Erro!",
        text: "Erro ao excluir o agendamento.",
        confirmButtonText: "OK",
        customClass: {
          confirmButton: "btn bg-prim",
        },
        buttonsStyling: false,
      });

      window.location.href = "/agendamentos/";
    }
  }

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
