$(document).ready(async function () {
  $(".select2").select2({
    placeholder: "Selecione uma opção",
    allowClear: true,
    width: "100%",
  });

  const API_URL = "http://127.0.0.1:8000";
  const endpoints = {
    grupos: "/grupos",
    mensagens: "/mensagens",
    conexoes: "/conexoes-ativas",
    departamentos: "/departamentos",
  };

  async function preencherSelect(endpoint, selectId) {
    try {
      const response = await fetch(API_URL + endpoint);
      const data = await response.json();
      const select = $(`#${selectId}`);
      select.empty();
      if (endpoint == "/grupos") {
        data.forEach((item) => {
          select.append(new Option(item.nome, item.id));
        });
      }
      else if (endpoint == "/mensagens") {
        data.forEach((item) => {
          select.append(new Option(item.title, item.id));
        });
      }
      else if (endpoint == "/conexoes-ativas" || endpoint == "/departamentos") {
        data.forEach((item) => {
          select.append(new Option(item.name, item.id));
        });
      }

      select.trigger("change");
    } catch (error) {
      console.error(`❌ Erro ao carregar ${selectId}:`, error);
    }
  }

  await preencherSelect(endpoints.grupos, "grupos");
  await preencherSelect(endpoints.mensagens, "mensagens");
  await preencherSelect(endpoints.conexoes, "conexao");
  await preencherSelect(endpoints.departamentos, "departamento");

  async function salvarAgendamento() {
    const grupoId = $("#grupos").val();
    const diaAgendamento = $("#horarioAgendamento").val();
    const ativo = $("#ativo").val();
    const mensagens = $("#mensagens").val().map(Number);
    const conexaoId = $("#conexao").val();
    const departamentoId = $("#departamento").val();

    const url = API_URL + "/agendamentos";
    const method = "POST";

    const grupoData = {
      grupo_id: grupoId,
      horario_disparo: diaAgendamento,
      ativo: ativo,
      conexao_id: conexaoId,
      departamento_id: departamentoId,
      mensagem_ids: mensagens,
    };

    try {
      const response = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(grupoData),
      });

      const result = await response.json();
      alert(result.message || result.error);
      if (!result.error) window.location.href = "/agendamentos/";
    } catch (error) {
      console.error("Erro:", error);
    }

    function limparCampos() {
      $("#grupos").val("");
      $("#horarioAgendamento").val("");
      $("#mensagens").val("");
    }
  }

  $("#salvarBtn").on("click", salvarAgendamento);
});
