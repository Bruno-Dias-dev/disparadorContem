$(document).ready(async function () {
    $(".select2").select2({
    placeholder: "Selecione uma opção",
    allowClear: true,
    width: "100%",
  });

  const API_URL = "http://127.0.0.1:8000";
  const endpoints = {
    grupos: "/grupos",
  };

  async function preencherSelect(endpoint, selectId) {
    try {
      const response = await fetch(API_URL + endpoint);
      const data = await response.json();
      const select = $(`#${selectId}`);
      select.empty();
      
      data.forEach((item) => {
        select.append(
          new Option(item.nome, item.id)
        );
      });

      select.trigger("change");
    } catch (error) {
      console.error(`❌ Erro ao carregar ${selectId}:`, error);
    }
  }

  await preencherSelect(endpoints.grupos, "grupos");

  async function salvarAgendamento() {
    const grupoId = $("#grupos").val();
    const diaAgendamento = $("#horarioAgendamento").val();
    const ativo = $("#ativo").val();

    const url = API_URL + "/agendamentos";
    const method = "POST";

    const grupoData = {
        grupo_id: grupoId,
        horario_disparo: diaAgendamento,
        ativo: ativo
    };
    try {
        const response = await fetch(url, {
          method: method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(grupoData),
        });
  
        const result = await response.json();
        alert(result.message || result.error);
        if (!result.error) limparCampos();
      } catch (error) {
        console.error("Erro:", error);
      }

    function limparCampos() {
        $("#grupos").val("");
        $("#horarioAgendamento").val("");
    }
  }

  $("#salvarBtn").on("click", salvarAgendamento);

});
