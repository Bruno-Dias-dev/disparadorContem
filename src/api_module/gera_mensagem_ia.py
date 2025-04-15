import os
from openai import OpenAI, Client
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Inicializa cliente OpenAI
#client = OpenAI(api_key=api_key)

client = Client()

def reescrever_mensagem(texto_original: str) -> str:
    """
    Reescreve uma mensagem mantendo o sentido, objetivo, tom e emojis,
    formatando com quebras de parágrafo claras para envio em aplicativos como WhatsApp.

    Args:
        texto_original (str): A mensagem original.

    Returns:
        str: Uma versão reformulada da mensagem.
    """
    prompt = (
        "Reescreva a seguinte mensagem de forma um pouco diferente, utilize sinonimos, sem perder o conteúdo, objetivo ou tom. "
        "Mantenha o uso de emojis — você pode trocá-los por equivalentes, mas nunca removê-los completamente. "
        "A mensagem deve ser organizada em parágrafos separados por quebras de linha claras, para facilitar a leitura no WhatsApp. "
        "Não adicione nem omita informações. Apenas reformule com um toque mais natural e humanizado:\n\n"
        f"{texto_original}"
    )

    try:
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "Você é um reescritor profissional de mensagens para WhatsApp. Sua escrita é clara, gentil, natural, com parágrafos bem definidos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=1000
        )

        texto_formatado = resposta.choices[0].message.content.strip()

        # Garante que haja espaçamento entre parágrafos
        texto_com_quebra = "\n\n".join(par.strip() for par in texto_formatado.split("\n") if par.strip())

        return texto_com_quebra

    except Exception as e:
        print(f"❌ Erro ao chamar OpenAI: {e}")
        return texto_original

