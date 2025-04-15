$(document).ready(function () {
  const pathSegments = window.location.pathname.split("/");
  const grupoId = pathSegments[pathSegments.length - 1];

  if (!grupoId || isNaN(grupoId)) {
    alert("Nenhum ID de grupo foi informado!");
    window.location.href = "/";
    return;
  }
  const tabela = $("#tabela-faturas").DataTable({
    ajax: {
      url: `http://127.0.0.1:8000/grupos/${grupoId}/faturas`,
      dataSrc: function (json) {
        return json.map((item) => ({
          codigo: item["código_da_fatura"],
          celular: item.celular,
        }));
      },
    },
    columns: [{ data: "codigo" }, { data: "celular" }],
    language: {
      url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
    },
    initComplete: function(settings, json) {
        const total = json?.length || 0;
        document.getElementById("total").textContent = total;
      }
  });

});
