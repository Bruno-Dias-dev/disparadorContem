import sys
import os
import streamlit as st
import requests
from src.api_module import mensagens

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


# st.set_page_config(page_title="Interface Backend", layout="centered")
st.set_page_config( 
    page_title="Grupo Contém", 
    page_icon=":dollar:", 
    layout="wide",
    initial_sidebar_state="collapsed"
) 
st.title("🚀 Interface com Backend em Streamlit")

# Campo de entrada do usuário
pagina = st.number_input("Digite o número da página:", min_value=1, value=1)
quantidade = st.number_input("Quantidade de mensagens por página:", min_value=1, value=50)

if st.button("Obter Mensagens"):
    try:
        # Chamando a função do backend
        resposta = mensagens.get_mensagens(page=pagina, qtd=quantidade)
        
        if "error" in resposta:
            st.error(f"❌ Erro: {resposta['error']}")
        else:
            st.success("✅ Mensagens carregadas com sucesso!")
            st.json(resposta)
    except Exception as e:
        st.error(f"⚠️ Erro ao conectar com o backend: {e}")
