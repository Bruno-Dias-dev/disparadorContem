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
      const data = await response.json();

      const select = $(`#${selectId}`);
      select.empty();

      data.forEach((item) => {
        select.append(
          new Option(Object.values(item)[0], Object.values(item)[0])
        );
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

  function getSelectedValues(selectId) {
    return $(`#${selectId}`).val() || [];
  }

  async function salvarGrupo() {
    const grupoId = $("#grupoId").val();
    const nome = $("#nome").val();
    const ativo = $("#ativo").val();
    const pdf = $("#pdf").val();

    // Captura múltiplos valores selecionados e converte em um objeto JSON válido
    function getSelectedJson(selectId) {
      const values = $(`#${selectId}`).val() || [];
      return values.length ? { valores: values } : null; // Converte para um dicionário válido
    }

    const convenios = getSelectedJson("convenios");
    const estipulantes = getSelectedJson("estipulantes");
    const statusContratos = getSelectedJson("statusContratos");
    const alertasContratos = getSelectedJson("alertasContratos");
    
    console.log(ativo);
    console.log(pdf);

    // Validação de campo obrigatório
    if (!nome.trim()) {
      alert("O nome do grupo é obrigatório!");
      return;
    }

    // Montar objeto JSON para envio
    const grupoData = {
      nome: nome,
      convenios: convenios,
      estipulantes: estipulantes,
      status_contratos: statusContratos,
      alertas_contratos: alertasContratos,
      ativo: ativo,
      pdf: pdf,
    };

    const url = grupoId
      ? `http://127.0.0.1:8000/grupos/${grupoId}`
      : `http://127.0.0.1:8000/grupos`;
    const method = grupoId ? "PUT" : "POST";

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
  }

  function limparCampos() {
    $("#grupoId").val("");
    $("#nome").val("");
    $(".select2").val(null).trigger("change");
  }

  // Associando eventos aos botões
  $("#salvarGrupoBtn").on("click", salvarGrupo);
  $("#limparCamposBtn").on("click", limparCampos);
});
