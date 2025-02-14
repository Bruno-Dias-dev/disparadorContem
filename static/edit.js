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
    window.location.href = "/grupos";
    return;
  }

  async function carregarGrupo() {
    try {
      const response = await fetch(`http://127.0.0.1:8000/grupos/${grupoId}`);
      if (!response.ok) throw new Error("Grupo não encontrado");

      const grupo = await response.json();
      document.getElementById("grupoId").value = grupo.id;
      document.getElementById("nome").value = grupo.nome;

      // Preenche os selects com todas as opções da API e as selecionadas
      await preencherSelect("convenios", grupo.convenios, "/convenios");
      await preencherSelect(
        "estipulantes",
        grupo.estipulantes,
        "/estipulantes"
      );
      await preencherSelect(
        "statusContratos",
        grupo.status_contratos,
        "/status-contrato"
      );
      await preencherSelect(
        "alertasContratos",
        grupo.alertas_contratos,
        "/alerta-contrato"
      );
    } catch (error) {
      alert(error.message);
      window.location.href = "/grupos";
    }
  }

  async function preencherSelect(selectId, selectedValues, endpoint) {
    console.log(
      `🔍 DEBUG - Valores selecionados para ${selectId}:`,
      selectedValues
    );

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

      console.log(
        `✅ DEBUG - Opções disponíveis para ${selectId}:`,
        allOptions
      );

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

  document
    .getElementById("salvarGrupoBtn")
    .addEventListener("click", async function () {
      const nome = document.getElementById("nome").value;
      const convenios = [
        ...document.getElementById("convenios").selectedOptions,
      ].map((opt) => opt.value);
      const estipulantes = [
        ...document.getElementById("estipulantes").selectedOptions,
      ].map((opt) => opt.value);
      const statusContratos = [
        ...document.getElementById("statusContratos").selectedOptions,
      ].map((opt) => opt.value);
      const alertasContratos = [
        ...document.getElementById("alertasContratos").selectedOptions,
      ].map((opt) => opt.value);

      const grupoData = {
        nome,
        convenios,
        estipulantes,
        status_contratos: statusContratos,
        alertas_contratos: alertasContratos,
      };

      try {
        const response = await fetch(`${API_URL}/grupos/${grupoId}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(grupoData),
        });

        const result = await response.json();
        alert(result.message || result.error);
        if (!result.error) window.location.href = "/grupos";
      } catch (error) {
        console.error("Erro ao salvar grupo:", error);
      }
    });

  carregarGrupo();
});
