const API_URL = "http://212.85.21.32:8000";

$(document).ready(async function () {
  $(".select2").select2({
    placeholder: "Selecione uma opção",
    allowClear: true,
    width: "100%",
  });

  console.log("API_URL:", API_URL);
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
    const tipoGrupo = $("#selectUpload").val();

    if (!nome) {
      await Swal.fire({
        icon: "warning",
        title: "Atenção!",
        text: "O nome do grupo é obrigatório!",
        confirmButtonText: "OK",
        customClass: {
          confirmButton: "btn bg-prim",
        },
        buttonsStyling: false,
      });
      return;
    }

    if (tipoGrupo === "1") {
      validarEEnviarArquivo(nome);
      return;
    } else {
      cadastrarGrupoEEnviarFaturas();
      return;
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
async function cadastrarGrupoEEnviarFaturas() {
  const grupoData = {
    nome,
    convenios: getSelectedJson("convenios"),
    estipulantes: getSelectedJson("estipulantes"),
    status_contratos: getSelectedJson("statusContratos"),
    alertas_contratos: getSelectedJson("alertasContratos"),
    ativo,
    pdf,
    fase: $("#qtdeDiasAtraso").val() || "0",
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

async function validarEEnviarArquivo(nomeGrupo) {
  const input = document.getElementById("arquivoExcel");
  const file = input.files[0];

  if (!file) {
    alert("Nenhum arquivo selecionado.");
    return;
  }

  const extensaoValida = file.name.endsWith(".xlsx");
  if (!extensaoValida) {
    alert("Por favor, envie um arquivo .xlsx");
    return;
  }

  const reader = new FileReader();

  reader.onload = async function (e) {
    const data = new Uint8Array(e.target.result);
    const workbook = XLSX.read(data, { type: "array" });

    const primeiraAba = workbook.SheetNames[0];
    const sheet = workbook.Sheets[primeiraAba];
    const json = XLSX.utils.sheet_to_json(sheet, { header: 1 });

    console.log("Conteúdo do arquivo:", json);

    // Adição da verificação para arquivo vazio ou sem dados
    if (!json || json.length === 0) {
      alert("O arquivo Excel está vazio ou não contém dados.");
      return;
    }

    const cabecalho = json[0];

    if (
      !cabecalho ||
      cabecalho[0]?.toLowerCase() !== "fatura" ||
      cabecalho[1]?.toLowerCase() !== "celular"
    ) {
      alert(
        "Arquivo inválido. A primeira coluna deve ser 'fatura', a segunda 'celular'."
      );
      return;
    }

    alert("Arquivo válido! Enviando para o servidor...");

    // Se válido, envia o arquivo para o backend via POST
    const formData = new FormData();
    formData.append("file", file); // O nome 'file' deve corresponder ao parâmetro do endpoint em Python
    formData.append("nome_grupo", nomeGrupo);
    try {
      const response = await fetch(`${API_URL}/upload_faturas_excel`, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        alert(result.message); // Exibe a mensagem de sucesso do backend
      } else {
        const errorData = await response.json();
        alert(
          `Erro ao enviar o arquivo: ${errorData.detail || response.statusText}`
        );
      }
    } catch (error) {
      console.error("Erro na requisição:", error);
      alert("Erro de rede ou servidor ao enviar o arquivo.");
    }
  };

  reader.readAsArrayBuffer(file);
}
