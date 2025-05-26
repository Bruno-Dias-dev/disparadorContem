const API_URL = "http://127.0.0.1:8000";

const ENDPOINTS = {
  convenios: "/convenios",
  estipulantes: "/estipulantes",
  statusContratos: "/status-contrato",
  alertasContratos: "/alerta-contrato",
  grupos: "/grupos",
  uploadFaturas: "/upload_faturas_excel",
};

// --- Funções Auxiliares ---

/**
 * Exibe um alerta usando SweetAlert2.
 * @param {string} icon - 'success', 'error', 'warning', 'info', 'question'
 * @param {string} title - Título do alerta.
 * @param {string} text - Mensagem do alerta.
 */
async function showAlert(icon, title, text) {
  await Swal.fire({
    icon: icon,
    title: title,
    text: text,
    confirmButtonText: "OK",
    customClass: {
      confirmButton: "btn bg-prim",
    },
    buttonsStyling: false,
  });
}

/**
 * Realiza uma requisição fetch e trata a resposta.
 * @param {string} url - URL da requisição.
 * @param {Object} options - Opções da requisição (method, headers, body, etc.).
 * @returns {Promise<Object>} - Dados da resposta em JSON.
 * @throws {Error} - Lança um erro se a resposta não for OK.
 */
async function fetchData(url, options) {
  const response = await fetch(url, options);
  const data = await response.json();

  if (!response.ok) {
    let errorMessage = "Ocorreu um erro na requisição.";
    if (data && typeof data.detail === "string") {
      errorMessage = data.detail;
    } else if (response.statusText) {
      errorMessage = response.statusText;
    } else if (data && typeof data === "object") {
      errorMessage = JSON.stringify(data);
    }
    throw new Error(errorMessage);
  }
  return data;
}

/**
 * Preenche um elemento select2 com dados da API.
 * @param {string} endpoint - Endpoint da API para buscar os dados.
 * @param {string} selectId - ID do elemento select HTML.
 */
async function preencherSelect(endpoint, selectId) {
  try {
    const data = await fetchData(API_URL + endpoint, { method: "GET" });
    const select = $(`#${selectId}`);
    select.empty();

    if (endpoint === ENDPOINTS.convenios) {
      select.append(new Option("Todos", "Todos"));
    }

    data.forEach((item) => {
      const value = Object.values(item)[0];
      select.append(new Option(value, value));
    });

    select.trigger("change");
  } catch (error) {
    console.error(`❌ Erro ao carregar ${selectId}:`, error);
    await showAlert(
      "error",
      "Erro de Carregamento",
      `Não foi possível carregar as opções para ${selectId}: ${error.message}`
    );
  }
}

/**
 * Retorna os valores selecionados de um select2 como um objeto JSON.
 * @param {string} selectId - ID do elemento select HTML.
 * @returns {Object} - Objeto com a chave `valores` contendo um array dos valores selecionados.
 */
function getSelectedJson(selectId) {
  const values = $(`#${selectId}`).val() || [];
  return { valores: values };
}

/**
 * Limpa os campos do formulário.
 */
function limparCampos() {
  $("#nome").val("");
  $(".select2").val(null).trigger("change");
  // Oculta o campo de fase/dias atraso se estiver visível
  $("#qtdeDiasAtraso").closest(".mb-3").addClass("d-none");
  $("#selectUpload").val(""); // Limpa o tipo de upload selecionado
  $("#arquivoExcel").val(""); // Limpa o input de arquivo
}

// --- Funções de Lógica Principal ---

/**
 * Cadastra um novo grupo no backend.
 * @returns {Promise<number|null>} - O ID do grupo cadastrado ou null em caso de erro.
 */
async function cadastrarGrupo() {
  const nome = $("#nome").val().trim();
  const ativo = $("#ativo").is(":checked");
  const pdf = $("#pdf").is(":checked");
  const fase = $("#qtdeDiasAtraso").val(); // String

  if (!nome) {
    await showAlert("warning", "Atenção!", "O nome do grupo é obrigatório!");
    return null;
  }

  const grupoData = {
    nome: nome,
    convenios: getSelectedJson("convenios"), // {"valores": ["..."]}
    estipulantes: getSelectedJson("estipulantes"),
    status_contratos: getSelectedJson("statusContratos"),
    alertas_contratos: getSelectedJson("alertasContratos"),
    ativo: ativo,
    pdf: pdf,
    fase: fase || "0",
  };
  console.log("Dados do grupo para cadastro:", grupoData);

  try {
    const result = await fetchData(API_URL + ENDPOINTS.grupos, {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // Continua sendo JSON
      },
      body: JSON.stringify(grupoData), // Objeto JS para JSON string
    });

    await showAlert(
      "success",
      "Sucesso!",
      result.message || "Grupo cadastrado com sucesso!"
    );
    return result.grupo_id;
  } catch (error) {
    console.error("Erro no cadastro do grupo:", error);
    // O `error.message` deve vir da função `WorkspaceData` com o detalhe do erro do backend
    await showAlert(
      "error",
      "Erro!",
      `Erro ao salvar o grupo: ${error.message}`
    );
    return null;
  }
}

/**
 * Valida o arquivo Excel e o envia para o backend com o ID e NOME do grupo.
 * @param {number} grupoId - O ID do grupo ao qual as faturas pertencem.
 * @param {string} nomeGrupo - O nome do grupo (para a coluna nome_grupo na fatura).
 */
async function validarEEnviarArquivo(grupoId, nomeGrupo) {
  const input = document.getElementById("arquivoExcel");
  const file = input.files[0];

  if (!file) {
    await showAlert(
      "warning",
      "Atenção!",
      "Nenhum arquivo de faturas selecionado."
    );
    return;
  }

  if (!file.name.endsWith(".xlsx")) {
    await showAlert("warning", "Atenção!", "Por favor, envie um arquivo .xlsx");
    return;
  }

  const reader = new FileReader();

  reader.onload = async function (e) {
    try {
      const data = new Uint8Array(e.target.result);
      const workbook = XLSX.read(data, { type: "array" });

      const primeiraAba = workbook.SheetNames[0];
      const sheet = workbook.Sheets[primeiraAba];
      const json = XLSX.utils.sheet_to_json(sheet, { header: 1 });

      console.log("Conteúdo do arquivo para validação:", json);

      if (!json || json.length === 0) {
        await showAlert(
          "warning",
          "Atenção!",
          "O arquivo Excel está vazio ou não contém dados."
        );
        return;
      }

      const cabecalho = json[0];
      if (
        !cabecalho ||
        cabecalho[0]?.toLowerCase() !== "fatura" ||
        cabecalho[1]?.toLowerCase() !== "celular"
      ) {
        await showAlert(
          "warning",
          "Atenção!",
          "Arquivo inválido. As colunas esperadas são 'fatura' e 'celular'."
        );
        return;
      }

      await showAlert(
        "info",
        "Processando...",
        "Arquivo de faturas válido! Enviando para o servidor..."
      );

      const formData = new FormData();
      formData.append("file", file);
      formData.append("grupo_id", grupoId); // Enviando o ID do grupo
      formData.append("nome_grupo", nomeGrupo); // Enviando o NOME do grupo

      const result = await fetchData(API_URL + ENDPOINTS.uploadFaturas, {
        method: "POST",
        body: formData,
      });

      await showAlert("success", "Sucesso!", result.message);
      limparCampos();
    } catch (error) {
      console.error("Erro na leitura ou envio do arquivo:", error);
      await showAlert(
        "error",
        "Erro!",
        `Erro ao processar/enviar arquivo de faturas: ${error.message}`
      );
    }
  };

  reader.readAsArrayBuffer(file);
}

/**
 * Função principal para lidar com o clique do botão "Salvar Grupo".
 * Orquestra a criação do grupo e, se aplicável, o upload das faturas.
 */
async function handleSalvarGrupoClick() {
  const tipoGrupo = $("#selectUpload").val();
  const nomeDoGrupoParaFaturas = $("#nome").val().trim();
  const grupoId = await cadastrarGrupo();

  // Se o grupo não foi criado com sucesso (grupoId é null), pare a execução.
  if (grupoId === null) {
    return;
  }

  if (tipoGrupo === "1") {
    await validarEEnviarArquivo(grupoId, nomeDoGrupoParaFaturas);
  } else {
    limparCampos();
    window.location.href = "/"; 
  }
}

// --- Inicialização do DOM e Event Listeners ---
$(document).ready(async function () {
  // Inicializa Select2
  $(".select2").select2({
    placeholder: "Selecione uma opção",
    allowClear: true,
    width: "100%",
  });

  console.log("API_URL:", API_URL);

  // Preenche os selects em paralelo (ou em série se a ordem for importante)
  await Promise.all([
    preencherSelect(ENDPOINTS.convenios, "convenios"),
    preencherSelect(ENDPOINTS.estipulantes, "estipulantes"),
    preencherSelect(ENDPOINTS.statusContratos, "statusContratos"),
    preencherSelect(ENDPOINTS.alertasContratos, "alertasContratos"),
  ]);

  // Event Listeners
  $("#salvarGrupoBtn").on("click", handleSalvarGrupoClick);
  $("#limparCamposBtn").on("click", limparCampos);

  // Lógica de exibição/ocultação do campo de fase/dias de atraso
  $("#statusContratos").on("change", function () {
    const statusSelecionado = $(this).val();
    const qtdeDiasAtrasoField = $("#qtdeDiasAtraso").closest(".mb-3");

    if (statusSelecionado && statusSelecionado.includes("Cancelado")) {
      qtdeDiasAtrasoField.removeClass("d-none");
    } else {
      qtdeDiasAtrasoField.addClass("d-none");
      $("#qtdeDiasAtraso").val(""); // Opcional: Limpa o valor quando ocultado
    }
  });

  // Lógica para mostrar/esconder o campo de upload de arquivo
  $("#selectUpload")
    .on("change", function () {
      const tipoSelecionado = $(this).val();
      if (tipoSelecionado === "1") {
        // Assumindo '1' é o valor para upload de arquivo
        $("#uploadArquivoContainer").removeClass("d-none"); // Assumindo que você tem um container para o input de arquivo
      } else {
        $("#uploadArquivoContainer").addClass("d-none");
        $("#arquivoExcel").val(""); // Limpa o input de arquivo ao esconder
      }
    })
    .trigger("change"); // Dispara no carregamento para ajustar o estado inicial
});
