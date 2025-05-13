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

      if (endpoint == "/convenios") {
        select.append(new Option("Todos", "Todos"));
      }
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

  function getSelectedJson(selectId) {
    const values = $(`#${selectId}`).val() || [];
    return { valores: values }; // Sempre retornar um objeto com a chave `valores`
  }

  async function salvarGrupo() {
    const nome = $("#nome").val().trim();
    const ativo = $("#ativo").is(":checked");
    const pdf = $("#pdf").is(":checked");

    if (!nome) {
      await Swal.fire({
        icon: "warning",
        title: "Atenção!",
        text: result.message || "O nome do grupo é obrigatório!",
        confirmButtonText: "OK",
        customClass: {
          confirmButton: "btn bg-prim",
        },
        buttonsStyling: false,
      });
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
      fase: $("#qtdeDiasAtraso").val(),
    };

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
      await Swal.fire({
        icon: "success",
        title: "Sucesso!",
        text: result.message || "Grupo cadastrado com sucesso!",
        confirmButtonText: "OK",
        customClass: {
          confirmButton: "btn bg-prim",
        },
        buttonsStyling: false,
      });
      window.location.href = "/"; // Redireciona após o cadastro
    } catch (error) {
        await Swal.fire({
        icon: "error",
        title: "Erro!",
        text: result.message || `Erro ao salvar o grupo: ${error.message}`,
        confirmButtonText: "OK",
        customClass: {
          confirmButton: "btn bg-prim",
        },
        buttonsStyling: false,
      });
    }
  }

  function limparCampos() {
    $("#nome").val("");
    $(".select2").val(null).trigger("change");
  }

  $("#salvarGrupoBtn").on("click", salvarGrupo);
  $("#limparCamposBtn").on("click", limparCampos);

  $("#statusContratos").on("change", function () {
    const statusSelecionado = $(this).val();
    console.log("Status selecionado:", statusSelecionado);

    if (statusSelecionado.includes("Cancelado")) {
      $("#qtdeDiasAtraso").closest(".mb-3").removeClass("d-none");

      // preencherSelect(endpoints.alertasContratos, "qtdeDiasAtraso");
    } else {
      // Oculta o select de Dias Em Atraso
      $("#qtdeDiasAtraso").closest(".mb-3").addClass("d-none");
    }
  });
});
