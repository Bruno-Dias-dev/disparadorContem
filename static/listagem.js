document.addEventListener("DOMContentLoaded", async function () {
  const API_URL = "http://212.85.21.32:8000";
  const listaGrupos = document.getElementById("listaGrupos");

  async function carregarGrupos() {
    try {
      const response = await fetch(`${API_URL}/grupos`);
      const grupos = await response.json();

      const tabela = $("#tbGrupos").DataTable({
        language: {
          url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json",
        },
      });
      tabela.clear();

      if (grupos.length === 0) {
        tabela.draw();
        return;
      }

      grupos.forEach((grupo) => {
        const trueFalse = grupo.ativo ? "Ativo" : "Inativo";
        const badgeColor = grupo.ativo ? "success" : "danger";

        tabela.row.add([
          grupo.id,
          grupo.nome,
          `<span class="badge bg-${badgeColor}">${trueFalse}</span>`,
          `
            <a href="/view/${grupo.id}" class="btn bg-prim btn-sm"><i class="bi bi-eye"></i></a>
            <a href="/edit/${grupo.id}" class="btn btn-primary btn-sm"><i class="bi bi-pencil"></i></a>
            <button class="btn btn-danger btn-sm btn-excluir" data-id="${grupo.id}"><i class="bi bi-trash"></i></button>
          `,
        ]);
      });

      tabela.draw(); // renderiza os dados na tabela
    } catch (error) {
      console.error("❌ Erro ao carregar grupos:", error);
    }
  }

  window.deletarGrupo = async function (id) {
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
  };

  listaGrupos.addEventListener("click", function (event) {
    if (event.target.closest(".btn-excluir")) {
      const id = event.target.closest(".btn-excluir").getAttribute("data-id");
      deletarGrupo(id);
    }
  });

  carregarGrupos();
});


