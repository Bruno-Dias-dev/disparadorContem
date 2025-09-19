const API_URL = "http://212.85.21.32:8000";

// Se ENDPOINTS for usado apenas para faturasGrupo aqui, pode ser simplificado
const ENDPOINTS = {
    faturasGrupo: (grupoId) => `${API_URL}/grupos/${grupoId}/faturas`, 
};

// --- Funções Auxiliares (Definidas no escopo global para serem acessíveis) ---

/**
 * Exibe um alerta usando SweetAlert2.
 * Esta função precisa ser acessível globalmente ou importada.
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

// Se a função fetchData também for usada neste arquivo para outras chamadas,
// ela também deveria ser definida globalmente ou importada aqui.
// Por exemplo:
/*
async function fetchData(url, options) {
    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
        console.error("Erro na resposta do servidor (detalhes):", data); 
        let errorMessage = "Ocorreu um erro na requisição.";
        if (data && typeof data.detail === 'string') {
            errorMessage = data.detail;
        } else if (response.statusText) {
            errorMessage = response.statusText;
        } else if (data && typeof data === 'object') {
            errorMessage = JSON.stringify(data);
        }
        throw new Error(errorMessage);
    }
    return data;
}
*/


$(document).ready(function () {
    const pathSegments = window.location.pathname.split("/");
    const grupoId = pathSegments[pathSegments.length - 1]; 

    if (!grupoId || isNaN(grupoId)) {
        showAlert("warning", "Atenção!", "Nenhum ID de grupo foi informado!");
        window.location.href = "/"; 
        return;
    }

    const tabela = $("#tabela-faturas").DataTable({
        ajax: {
            url: ENDPOINTS.faturasGrupo(grupoId), 
            dataSrc: function (json) {
                console.log("Dados recebidos do backend para o DataTables:", json);
                
                if (Array.isArray(json)) {
                    return json.map((item) => ({
                        codigo: item["codigo_da_fatura"], 
                        celular: item.celular,
                        dias_em_atraso: item.qtde_dias_atraso, 
                    }));
                } else if (json && json.message) {
                    console.warn("Backend retornou mensagem, não dados de faturas:", json.message);
                    return []; 
                }
                return []; 
            },
            error: function (xhr, error, thrown) {
                console.error("Erro no AJAX do DataTables:", xhr, error, thrown);
                showAlert("error", "Erro ao carregar faturas!", "Não foi possível carregar as faturas. Tente novamente mais tarde.");
            }
        },
        columns: [
            { data: "codigo" },
            { data: "celular" },
            { data: "dias_em_atraso" }
        ],
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
        },
        initComplete: function(settings, json) {
            const total = Array.isArray(json) ? json.length : 0; 
            document.getElementById("total").textContent = total; 
        }
    });

});