$(document).ready(async function () {
    $(".select2").select2({
      placeholder: "Selecione uma opção",
      allowClear: true,
      width: "100%",
    });
  
    const API_URL = "http://127.0.0.1:8000";
  
    async function salvarMensagem() {
      const mensagem = $("#mensagem").val().trim();
      const titulo = $("#titulo").val().trim();
      const ativo = $("#ativo").is(":checked");
  
      if (!mensagem) {
        alert("A mensagem é obrigatória!");
        return;
      }
  
      const mensagemData = {
        mensagem,
        ativo,
        titulo
      };
    
      try {
        const response = await fetch(`${API_URL}/mensagens`, {
          method: "POST",
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
  });
  