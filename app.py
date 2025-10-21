import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Controle de Horas", layout="wide")

# ===== Senha mestra =====
senha_mestra = "1b1m"

# ===== Inicializa session_state =====
if "usuarios" not in st.session_state:
    st.session_state.usuarios = {
        "Lucas Uva": {"senha": "lu123", "horas": [], "faltas": []},
        "Luis": {"senha": "lu1", "horas": [], "faltas": []},
        "Matheus": {"senha": "ma123", "horas": [], "faltas": []},
        "Raphaela": {"senha": "ra123", "horas": [], "faltas": []},
        "Ralf": {"senha": "ra1", "horas": [], "faltas": []},
        "Julia": {"senha": "ju1", "horas": [], "faltas": []},
        "Withyna": {"senha": "wi1", "horas": [], "faltas": []},
        "Melissa": {"senha": "me1", "horas": [], "faltas": []},
        "Ana": {"senha": "an1", "horas": [], "faltas": []},
        "Leandro": {"senha": "le1", "horas": [], "faltas": []},
    }

usuarios = st.session_state.usuarios  # usar session_state

# ===== Funções =====
def adicionar_horas(nome):
    st.subheader(f"Adicionar horas - {nome}")
    senha = st.text_input("Senha:", type="password", key=f"add_{nome}")
    if senha == usuarios[nome]["senha"]:
        dia = st.date_input("Escolha o dia da falta", key=f"data_add_{nome}")
        dia_str = dia.strftime("%d/%m/%Y")
        if st.button("Confirmar adição", key=f"btn_add_{nome}"):
            if dia_str not in usuarios[nome]["faltas"]:
                valor = 5 if dia.weekday() < 5 else 4
                usuarios[nome]["horas"].append(valor)
                usuarios[nome]["faltas"].append(dia_str)
                st.success(f"{valor} horas adicionadas em {dia_str}")
            else:
                st.warning("Essa data já foi registrada.")
    elif senha:
        st.error("Senha incorreta!")

def remover_horas_admin():
    st.subheader("🔒 Remover horas (Admin)")
    senha = st.text_input("Senha mestra:", type="password", key="senha_rem_admin")
    if senha == senha_mestra:
        nome = st.selectbox("Escolha o usuário:", list(usuarios.keys()))
        if usuarios[nome]["horas"]:
            qtd = st.number_input(
                "Quantas horas deseja remover?",
                min_value=1,
                max_value=sum(usuarios[nome]["horas"]),
                key=f"qtd_rem_admin_{nome}"
            )
            if st.button("Remover horas", key=f"btn_rem_admin_{nome}"):
                total_horas = sum(usuarios[nome]["horas"])
                if qtd <= total_horas:
                    horas_restantes = qtd
                    while horas_restantes > 0 and usuarios[nome]["horas"]:
                        if usuarios[nome]["horas"][-1] <= horas_restantes:
                            horas_restantes -= usuarios[nome]["horas"][-1]
                            usuarios[nome]["horas"].pop()
                            usuarios[nome]["faltas"].pop()
                        else:
                            usuarios[nome]["horas"][-1] -= horas_restantes
                            horas_restantes = 0
                    st.success(f"{qtd} horas removidas de {nome}")
                else:
                    st.error("Não há horas suficientes para remover.")
        else:
            st.warning("Esse usuário não possui horas a remover.")
    elif senha:
        st.error("Senha mestra incorreta!")

def ver_horas():
    st.subheader("📊 Horas devidas")
    for nome, dados in usuarios.items():
        with st.expander(f"{nome} - {sum(dados['horas'])} horas"):
            if dados["faltas"]:
                for dia, h in zip(dados["faltas"], dados["horas"]):
                    st.write(f"{dia}: {h} horas")
            else:
                st.write("Nenhuma falta registrada.")

def admin_panel():
    st.subheader("🔒 Painel Admin")
    senha = st.text_input("Senha mestra:", type="password", key="senha_admin")
    if senha == senha_mestra:
        op = st.selectbox("Escolha a operação:", ["Adicionar usuário", "Remover usuário", "Alterar senha"])
        
        if op == "Adicionar usuário":
            nome_novo = st.text_input("Nome do novo usuário")
            senha_inicial = st.text_input("Senha inicial")
            if st.button("Adicionar"):
                if nome_novo not in usuarios:
                    usuarios[nome_novo] = {"senha": senha_inicial, "horas": [], "faltas": []}
                    st.success(f"Usuário {nome_novo} adicionado!")
                else:
                    st.error("Usuário já existe.")

        elif op == "Remover usuário":
            nome_remover = st.selectbox("Escolha o usuário para remover:", list(usuarios.keys()))
            if st.button("Remover"):
                usuarios.pop(nome_remover)
                st.success(f"Usuário {nome_remover} removido!")

        elif op == "Alterar senha":
            nome_alt = st.selectbox("Escolha o usuário para alterar senha:", list(usuarios.keys()))
            nova_senha = st.text_input("Nova senha")
            if st.button("Alterar"):
                usuarios[nome_alt]["senha"] = nova_senha
                st.success(f"Senha de {nome_alt} alterada!")
    elif senha:
        st.error("Senha mestra incorreta!")

# ===== Interface Principal =====
st.title("⏱ Controle de Horas Devidas")

acao = st.radio("Escolha uma ação:", ["Adicionar horas", "Remover horas (Admin)", "Ver horas", "Admin"])

if acao == "Adicionar horas":
    nome = st.selectbox("Escolha seu nome:", list(usuarios.keys()))
    adicionar_horas(nome)

elif acao == "Remover horas (Admin)":
    remover_horas_admin()

elif acao == "Ver horas":
    ver_horas()

else:
    admin_panel()
