document.addEventListener("DOMContentLoaded", async function () {
  const API_URL = "http://127.0.0.1:8000";
  const listaGrupos = document.getElementById("listaGrupos");

  async function carregarGrupos() {
    try {
      const response = await fetch(`${API_URL}/grupos`);
      const grupos = await response.json();

      if (grupos.length === 0) {
        listaGrupos.innerHTML = `<p class="text-muted">Nenhum grupo cadastrado.</p>`;
        return;
      }

      listaGrupos.innerHTML = ""; // Limpa antes de renderizar
      grupos.forEach((grupo) => {
        const trueFalse = grupo.ativo ? "Ativo" : "Inativo";
        const badgeColor = grupo.ativo ? "success" : "danger";

        // Criando a linha da tabela
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${grupo.id}</td>
            <td>${grupo.nome}</td>
            <td><span class="badge bg-${badgeColor}">${trueFalse}</span></td>
            <td>            
              <a href="/view/${grupo.id}" class="btn bg-prim btn-sm">
                    <i class="bi bi-eye"></i> 
                </a>                
                <a href="/edit/${grupo.id}" class="btn btn-primary btn-sm">
                    <i class="bi bi-pencil"></i> 
                </a>
                <button class="btn btn-danger btn-sm btn-excluir" data-id="${grupo.id}">
                    <i class="bi bi-trash"></i> 
                </button>
            </td>
        `;

        listaGrupos.appendChild(row);
      });
    } catch (error) {
      console.error("❌ Erro ao carregar grupos:", error);
    }
  }

  window.deletarGrupo = async function (id) {
    if (!confirm("Tem certeza que deseja excluir este grupo?")) return;

    try {
      const response = await fetch(`${API_URL}/grupos/${id}`, {
        method: "DELETE",
      });

      const result = await response.json();
      alert(result.message || result.error);

      if (!result.error) carregarGrupos();
    } catch (error) {
      console.error("Erro ao excluir grupo:", error);
    }
  };

  listaGrupos.addEventListener("click", function (event) {
    if (event.target.closest(".btn-excluir")) {
      const id = event.target.closest(".btn-excluir").getAttribute("data-id");
      deletarGrupo(id);
    }
  });

  carregarGrupos();
});

// document.addEventListener("DOMContentLoaded", async function () {

//   const API_URL = "http://127.0.0.1:8000";
//   const listaGrupos = document.getElementById("listaGrupos");

//   async function carregarGrupos() {
//     try {
//       const response = await fetch(`${API_URL}/grupos`);
//       const grupos = await response.json();

//       if (grupos.length === 0) {
//         listaGrupos.innerHTML = `<p class="text-muted">Nenhum grupo cadastrado.</p>`;
//         return;
//       }

//       listaGrupos.innerHTML = ""; // Limpa antes de renderizar
//       grupos.forEach((grupo) => {
//         const trueFalse = grupo.ativo ? "Ativo" : "Inativo";
//         const badgeColor = grupo.ativo ? "success" : "danger";

//         // Criando a linha da tabela
//         const row = document.createElement("tr");
//         row.innerHTML = `
//             <td>${grupo.nome}</td>
//             <td><span class="badge bg-${badgeColor}">${trueFalse}</span></td>
//             <td>
//                 <a href="/edit/${grupo.id}" class="btn btn-primary btn-sm">
//                     <i class="bi bi-pencil"></i>
//                 </a>
//                 <button class="btn btn-danger btn-sm" onclick="deletarGrupo(${grupo.id})">
//                     <i class="bi bi-trash"></i>
//                 </button>
//             </td>
//         `;

//         listaGrupos.appendChild(row);
//       });

//       // card.innerHTML = `
//       //             <div class="card mb-3">
//       //                 <div class="card-body">
//       //                     <h5 class="card-title">${
//       //                       grupo.nome
//       //                     }</h5>
//       //                     <p class="text-muted">Criado em: ${formatarData(
//       //                       grupo.created
//       //                     )}</p>
//       //                     <div class="justify-content-between">
//       //                     <a href="/edit/${
//       //                       grupo.id
//       //                     }" class="btn btn-primary"><i class="bi bi-pencil"></i> Editar
//       //                     </a>
//       //                     <span class="badge text-bg-${badgeColor}">${trueFalse}</span>
//       //                     </div>

//       //                 </div>
//       //             </div>
//       //         `;
//     } catch (error) {
//       console.error("❌ Erro ao carregar grupos:", error);
//     }
//   }
//   // <button class="btn btn-danger btn-sm" onclick="deletarGrupo(${grupo.id})"><i class="bi bi-trash"></i> Excluir</button>

//   // Formatar listas para exibição
//   function formatarLista(valor) {
//     return valor ? (Array.isArray(valor) ? valor.join(", ") : valor) : "Nenhum";
//   }

//   // Formatar data para exibição
//   function formatarData(data) {
//     return data ? new Date(data).toLocaleDateString("pt-BR") : "Desconhecido";
//   }

//   // Redirecionar para a página de edição
//   function editarGrupo(id) {
//     alert("edit");
//     window.location.href = `edit.html?grupoId=${id}`;
//   }

//   // Excluir um grupo
//   async function deletarGrupo(id) {
//     if (!confirm("Tem certeza que deseja excluir este grupo?")) return;

//     try {
//       const response = await fetch(`${API_URL}/grupos/${id}`, {
//         method: "DELETE",
//       });

//       const result = await response.json();
//       alert(result.message || result.error);

//       if (!result.error) carregarGrupos();
//     } catch (error) {
//       console.error("Erro ao excluir grupo:", error);
//     }
//   }

//   carregarGrupos();
// });
