import streamlit as st

# -------------------------
# PERGUNTAS + REGRAS
# -------------------------
perguntas = [
    {
        "id": "aceite_prazo",
        "pergunta": "Aceite Urbanístico deferido dentro do prazo?",
        "opcoes": ["Sim", "Não"],
        "regras": {
            "Não": {
                "tipo": "inconformidade",
                "texto": "Apresentar Aceite urbanístico aprovado, dentro do prazo de validade."
            }
        }
    },
    {
        "id": "alteracao_lotes",
        "pergunta": "Alterou a quantidade de lotes aprovado no Aceite urbanístico?",
        "opcoes": ["Não", "Sim"],
        "regras": {
            "Sim": {
                "tipo": "inconformidade",
                "texto": "Deverá retornar à análise do aceite urbanístico para compatibilização do empreendimento. Obs¹ – verificar compatibilidade dos projetos de redes de água, esgoto, drenagem, licenciamento ambiental e acesso viário."
            }
        }
    }
]

# -------------------------
# FUNÇÕES
# -------------------------
def analisar(respostas, perguntas):
    inconformidades = []

    for p in perguntas:
        r = respostas[p["id"]]

        if r in p.get("regras", {}):
            regra = p["regras"][r]
            inconformidades.append(regra["texto"])

    return inconformidades


def definir_conclusao(inconformidades):
    if inconformidades:
        return "DESFAVORÁVEL"
    return "FAVORÁVEL"


def gerar_parecer(dados, inconformidades, conclusao):

    texto = f"""
PARECER DE ANÁLISE URBANÍSTICA

N° Protocolo: {dados['protocolo']}
Tipo do Empreendimento: {dados['tipo']}
Requerente: {dados['interessado']}
Número de Lotes: {dados['n_lotes']}

ANÁLISE
"""

    if not inconformidades:
        texto += "\nO empreendimento atende aos critérios analisados."

    if inconformidades:
        texto += "\n\nINCONFORMIDADES:\n"
        for i, item in enumerate(inconformidades, 1):
            texto += f"{i}. {item}\n"

    texto += f"""

CONCLUSÃO

Diante do exposto, o parecer é {conclusao}.
"""

    return texto


# -------------------------
# INTERFACE
# -------------------------
st.title("Gerador de Parecer Urbanístico")

st.header("Dados do Empreendimento")

protocolo = st.text_input("N° Protocolo")
tipo = st.selectbox("Tipo do Empreendimento", ["Loteamento", "Condomínio fechado de lotes"])
interessado = st.text_input("Nome do Requerente/Interessado")
n_lotes = st.number_input("Número de Lotes", min_value=1)

st.header("Análise")

respostas = {}

for p in perguntas:
    respostas[p["id"]] = st.selectbox(p["pergunta"], p["opcoes"])

# -------------------------
# EXECUÇÃO
# -------------------------
if st.button("Gerar Parecer"):

    dados = {
        "protocolo": protocolo,
        "tipo": tipo,
        "interessado": interessado,
        "n_lotes": n_lotes
    }

    inconformidades = analisar(respostas, perguntas)
    conclusao = definir_conclusao(inconformidades)

    parecer = gerar_parecer(dados, inconformidades, conclusao)

    st.text_area("Parecer Gerado", parecer, height=300)