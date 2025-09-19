$(document).ready(async function () {
    
    
  const API_URL = "http://212.85.21.32:8000";

  const pathSegments = window.location.pathname.split("/");
  const msg_id = pathSegments[pathSegments.length - 1];
  if (!msg_id || isNaN(msg_id)) {
    alert("Nenhum ID de mensagem foi informado!");
    window.location.href = "/mensagens/";
    return;
  }

  async function carregarMensagens() {
    try {
      const response = await fetch(`${API_URL}/mensagens/view/${msg_id}`);
      if (!response.ok) throw new Error("Mensagem não encontrada");
      const mensagem = await response.json();

      document.getElementById("titulo").value = mensagem.title;
      document.getElementById("mensagem").value = mensagem.mensagem;
      document.getElementById("ativo").checked = !!mensagem.ativo;

    } catch (error) {
      alert(error.message);
      window.location.href = "/mensagens/";
    }
  }

    async function salvarMensagem() {
      const mensagem = $("#mensagem").val().trim();
      const titulo = $("#titulo").val().trim();
      const ativo = $("#ativo").is(":checked");
  
      if (!mensagem) {
        alert("A mensagem é obrigatória!");
        return;
      }
      if (!titulo) {
        alert("A mensagem é obrigatória!");
        return;
      }
  
      const mensagemData = {
        msg_id,
        mensagem,
        ativo,
        titulo
      };
    
      try {
        const response = await fetch(`${API_URL}/mensagens/${msg_id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(mensagemData),
        });
  
        const result = await response.json();
  
        if (!response.ok) {
          throw new Error(result.error || "Erro ao salvar o grupo.");
        }
  
        alert("Mensagem cadastrada com sucesso!");
        window.location.href = "/mensagens/"; // Redireciona após o cadastro
      } catch (error) {
        console.error("Erro:", error);
        alert(`Erro ao salvar o grupo: ${error.message}`);
      }
    }
  
    function limparCampos() {
      $("#mensagem").val("");
      $("#titulo").val("");
    }
  
    $("#salvarMsgBtn").on("click", salvarMensagem);
    $("#limparCamposBtn").on("click", limparCampos);
    carregarMensagens();
  });
  