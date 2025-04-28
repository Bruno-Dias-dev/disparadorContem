document.addEventListener("DOMContentLoaded", async function () {
  $(".select2").select2({
    placeholder: "Selecione uma opção",
    allowClear: true,
    width: "100%",
  });

  const API_URL = "http://127.0.0.1:8000";
  const pathSegments = window.location.pathname.split("/");
  const grupoId = pathSegments[pathSegments.length - 1];

  if (!grupoId || isNaN(grupoId)) {
    alert("Nenhum ID de grupo foi informado!");
    window.location.href = "/";
    return;
  }

  async function carregarGrupo() {
    try {
      const response = await fetch(`http://127.0.0.1:8000/grupos/${grupoId}`);
      if (!response.ok) throw new Error("Grupo não encontrado");

      const grupo = await response.json();
      document.getElementById("grupoId").value = grupo.id;
      document.getElementById("nome").value = grupo.nome;
      document.getElementById("ativo").checked = !!grupo.ativo;
      document.getElementById("pdf").checked = !!grupo.pdf;

      // Preenche os selects com todas as opções da API e as selecionadas
      await preencherSelect("convenios", grupo.convenios, "/convenios");
      await preencherSelect(
        "estipulantes",
        grupo.estipulantes || { valores: [] },
        "/estipulantes"
      );
      await preencherSelect(
        "statusContratos",
        grupo.status_contratos || { valores: [] },
        "/status-contrato"
      );
      await preencherSelect(
        "alertasContratos",
        grupo.alertas_contratos || { valores: [] },
        "/alerta-contrato"
      );
    } catch (error) {
      alert(error.message);
      window.location.href = "/";
    }
  }

  async function preencherSelect(selectId, selectedValues, endpoint) {
    const select = document.getElementById(selectId);
    select.innerHTML = ""; // Limpa antes de preencher

    // Se `selectedValues` vier como um objeto {valores: [...]}, extrair a lista
    if (
      typeof selectedValues === "object" &&
      !Array.isArray(selectedValues) &&
      selectedValues.valores
    ) {
      selectedValues = selectedValues.valores;
    } else if (typeof selectedValues === "string") {
      selectedValues = selectedValues.includes(",")
        ? selectedValues.split(",").map((v) => v.trim())
        : [selectedValues];
    } else if (!Array.isArray(selectedValues)) {
      selectedValues = [];
    }

    try {
      // Buscar todas as opções da API
      const response = await fetch(`http://127.0.0.1:8000${endpoint}`);
      const allOptions = await response.json();
    
      // Adiciona todas as opções ao select
      allOptions.forEach((item) => {
        const value = Object.values(item)[0]; // Pega o valor do JSON retornado
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;

        // Se o valor já estava selecionado, marcar como `selected`
        if (selectedValues.includes(value)) {
          option.selected = true;
        }

        select.appendChild(option);
      });

      // Atualiza o Select2 após preencher os valores
      $(`#${selectId}`).trigger("change");
    } catch (error) {
      console.error(`❌ Erro ao carregar opções para ${selectId}:`, error);
    }
  }

  function getSelectedJson(selectId) {
    const values = $(`#${selectId}`).val() || [];
    return values.length ? { valores: values } : null; // Converte para um dicionário válido
  }

  document
    .getElementById("salvarGrupoBtn")
    .addEventListener("click", async function () {
      const grupoId = $("#grupoId").val();
      const nome = $("#nome").val();
      const ativo = $("#ativo").is(":checked");
      const pdf = $("#pdf").is(":checked");

      // Captura múltiplos valores selecionados e converte em um objeto JSON válido
      function getSelectedJson(selectId) {
        const values = $(`#${selectId}`).val() || [];
        return { valores: values }; 
      }

      const convenios = getSelectedJson("convenios");
      const estipulantes = getSelectedJson("estipulantes");
      const statusContratos = getSelectedJson("statusContratos");
      const alertasContratos = getSelectedJson("alertasContratos");

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

      const url = `http://127.0.0.1:8000/grupos/${grupoId}`;
      const method = "PUT";

      try {
        const response = await fetch(url, {
          method: method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(grupoData),
        });

        const result = await response.json();
        alert(result.message || result.error);
        if (!result.error) window.location.href = "/";
      } catch (error) {
        console.error("Erro:", error);
      }
    });

  carregarGrupo();
});
