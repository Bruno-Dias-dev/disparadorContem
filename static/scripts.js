$(document).ready(async function () {
  $(".select2").select2({
    placeholder: "Selecione uma opção",
    allowClear: true,
    width: "100%",
  });

  const API_URL = "http://127.0.0.1:8000";
  const endpoints = {
    convenios: "/convenios",
    estipulantes: "/estipulantes",
    statusContratos: "/status-contrato",
    alertasContratos: "/alerta-contrato",
  };

  async function preencherSelect(endpoint, selectId) {
    try {
      const response = await fetch(API_URL + endpoint);
      if (!response.ok) throw new Error(`Erro ao carregar ${selectId}`);
      
      const data = await response.json();
      const select = $(`#${selectId}`);
      select.empty();

      data.forEach((item) => {
        select.append(new Option(Object.values(item)[0], Object.values(item)[0]));
      });

      select.trigger("change");
    } catch (error) {
      console.error(`❌ Erro ao carregar ${selectId}:`, error);
    }
  }

  await preencherSelect(endpoints.convenios, "convenios");
  await preencherSelect(endpoints.estipulantes, "estipulantes");
  await preencherSelect(endpoints.statusContratos, "statusContratos");
  await preencherSelect(endpoints.alertasContratos, "alertasContratos");

  function getSelectedJson(selectId) {
    const values = $(`#${selectId}`).val() || [];
    return { valores: values }; // Sempre retornar um objeto com a chave `valores`
  }

  async function salvarGrupo() {
    const nome = $("#nome").val().trim();
    const ativo = $("#ativo").is(":checked");
    const pdf = $("#pdf").is(":checked");

    if (!nome) {
      alert("O nome do grupo é obrigatório!");
      return;
    }

    const grupoData = {
      nome,
      convenios: getSelectedJson("convenios"),
      estipulantes: getSelectedJson("estipulantes"),
      status_contratos: getSelectedJson("statusContratos"),
      alertas_contratos: getSelectedJson("alertasContratos"),
      ativo,
      pdf,
    };

    console.log("Enviando dados:", grupoData);

    try {
      const response = await fetch(`${API_URL}/grupos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(grupoData),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Erro ao salvar o grupo.");
      }

      alert("Grupo cadastrado com sucesso!");
      window.location.href = "/"; // Redireciona após o cadastro
    } catch (error) {
      console.error("Erro:", error);
      alert(`Erro ao salvar o grupo: ${error.message}`);
    }
  }

  function limparCampos() {
    $("#nome").val("");
    $(".select2").val(null).trigger("change");
  }

  $("#salvarGrupoBtn").on("click", salvarGrupo);
  $("#limparCamposBtn").on("click", limparCampos);
});
