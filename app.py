import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Controladoria & Gestão Executiva | Muller Oliveira", 
    page_icon="⚖️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PERSISTÊNCIA DE USUÁRIOS EM JSON (AUTONOMIA TOTAL) ---
USER_FILE = "usuarios.json"

def carregar_usuarios():
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "admin": {"senha": "muller2026", "nome": "Muller Oliveira", "tipo": "admin"},
        "escritorio_a": {"senha": "123", "nome": "T.A. Advocacia", "tipo": "cliente"},
        "nayeralira": {"senha": "nayara26", "nome": "NAYARA LIRA ADVOCACIA PREVIDENCIÁRIA", "tipo": "cliente"}
    }

def salvar_usuarios(usuarios):
    try:
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Erro ao salvar arquivo de usuários: {e}")

if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = carregar_usuarios()

if 'base_dados_geral' not in st.session_state:
    st.session_state['base_dados_geral'] = {
        "T.A. Advocacia": {},
        "NAYARA LIRA ADVOCACIA PREVIDENCIÁRIA": {}
    }

if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = None

if 'modo_gerenciar' not in st.session_state:
    st.session_state['modo_gerenciar'] = False

# --- DESIGN SYSTEM: SOFTWARE EXECUTIVO PREMIUM (TEMA CLARO & CHAMPAGNE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg: #F6F7F9;
        --sidebar: #1D2633;
        --sidebar-hover: #253142;
        --surface: #FFFFFF;
        --surface-soft: #F1F3F5;
        --border: #E2E5E9;
        --border-dark: #344154;
        --text: #202632;
        --text-secondary: #6E7684;
        --text-muted: #8A919D;
        --text-dark-bg: #F4F5F7;
        --text-dark-bg-secondary: #AEB6C2;
        --accent: #B89A6A;
        --accent-hover: #A8895D;
        --success: #59806A;
        --danger: #A45F5F;
        --warning: #B38B56;
        --radius-input: 9px;
        --radius-button: 9px;
        --radius-card: 12px;
    }

    .stApp {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }

    section[data-testid="stSidebar"] {
        background-color: var(--sidebar) !important;
        border-right: 1px solid var(--border-dark) !important;
        padding-top: 1rem !important;
    }
    section[data-testid="stSidebar"] * {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-dark-bg) !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: var(--border-dark) !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="input"] input, 
    section[data-testid="stSidebar"] div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] .stNumberInput input, 
    section[data-testid="stSidebar"] .stTextInput input {
        color: #202632 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text) !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }

    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: var(--surface) !important;
        border-radius: var(--radius-input) !important;
        border: 1px solid var(--border) !important;
        min-height: 42px !important;
    }
    div[data-baseweb="input"] input, div[data-baseweb="select"] span {
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
    }
    .stNumberInput input, .stTextInput input {
        background-color: var(--surface) !important;
        color: var(--text) !important;
        border-radius: var(--radius-input) !important;
        border: 1px solid var(--border) !important;
        font-size: 14px !important;
        height: 42px !important;
    }

    div[data-testid="stForm"] {
        background-color: var(--surface) !important;
        padding: 24px !important;
        border-radius: var(--radius-card) !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 1px 3px rgba(31, 38, 50, 0.04);
    }

    [data-testid="stMetric"] {
        background-color: var(--surface) !important;
        padding: 18px 20px !important;
        border-radius: var(--radius-card) !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 1px 3px rgba(31, 38, 50, 0.04);
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-size: 34px !important;
        font-weight: 650 !important;
        letter-spacing: -0.03em;
        line-height: 1.1 !important;
    }

    .stButton > button[kind="primary"], div.stButton > button:first-child {
        background-color: var(--accent) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: var(--radius-button) !important;
        font-weight: 600 !important;
        height: 42px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover, div.stButton > button:first-child:hover {
        background-color: var(--accent-hover) !important;
        color: #FFFFFF !important;
    }

    .stButton > button[kind="secondary"] {
        background-color: var(--surface) !important;
        border: 1px solid var(--border) !important;
        color: #3C4450 !important;
        border-radius: var(--radius-button) !important;
        height: 40px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: var(--surface-soft) !important;
        border-color: #C5CACF !important;
        color: var(--text) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
        background-color: transparent !important;
        border-bottom: 1px solid var(--border) !important;
        margin-bottom: 28px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: var(--text-muted) !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        padding: 8px 4px 12px 4px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text) !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--text) !important;
        border-bottom: 2px solid var(--accent) !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- TELA DE AUTENTICAÇÃO EXECUTIVA ---
if st.session_state['usuario_logado'] is None:
    st.markdown("""
        <div style="max-width: 400px; margin: 100px auto; background-color: #FFFFFF; padding: 40px; border-radius: 14px; border: 1px solid #E2E5E9; box-shadow: 0 4px 20px rgba(31, 38, 50, 0.06); text-align: center;">
            <h2 style="color: #202632; margin-bottom: 4px; font-size: 28px; font-weight: 650; letter-spacing: -0.02em;">Muller Oliveira</h2>
            <p style="color: #6E7684; font-size: 10px; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 32px; font-weight: 600;">Controladoria & Gestão Executiva</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_col, col_l2 = st.columns([1, 1.2, 1])
    with col_col:
        aba_login, aba_rec = st.tabs(["Acesso", "Recuperar"])
        
        with aba_login:
            with st.form("form_login"):
                st.markdown("<p style='font-size: 13px; color: #6E7684; margin-bottom: 12px;'>Entre com suas credenciais corporativas.</p>", unsafe_allow_html=True)
                usuario_input = st.text_input("Usuário de acesso")
                senha_input = st.text_input("Senha", type="password")
                entrar = st.form_submit_button("Acessar plataforma", type="primary", use_container_width=True)
                
                if entrar:
                    u_clean = usuario_input.strip().lower()
                    s_clean = senha_input.strip()
                    usuarios_dict = carregar_usuarios()
                    if u_clean in usuarios_dict and usuarios_dict[u_clean]['senha'] == s_clean:
                        st.session_state['usuario_logado'] = u_clean
                        st.session_state['usuarios'] = usuarios_dict
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas. Verifique usuário e senha.")
                        
        with aba_rec:
            st.markdown("<p style='font-size: 13px; color: #6E7684; margin-top: 10px;'>Solicite o reestabelecimento ao administrador.</p>", unsafe_allow_html=True)
            user_rec = st.text_input("Usuário cadastrado", key="rec_user")
            if st.button("Enviar solicitação", type="secondary", use_container_width=True):
                usuarios_dict = carregar_usuarios()
                if user_rec.strip().lower() in usuarios_dict:
                    st.success("Solicitação enviada com sucesso.")
                else:
                    st.warning("Usuário não localizado.")
    st.stop()

# --- SESSÃO ATIVA & SIDEBAR ORGANIZADA ---
user_atual = st.session_state['usuario_logado']
st.session_state['usuarios'] = carregar_usuarios()
dados_user = st.session_state['usuarios'][user_atual]
is_admin = dados_user['tipo'] == 'admin'

tipo_usuario_str = 'Administrador' if is_admin else 'Cliente Corporativo'

st.sidebar.markdown("<div style='font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600; color: #8F98A6; margin-bottom: 6px;'>Sessão</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"""
    <div style="margin-bottom: 12px;">
        <div style="font-size: 14px; font-weight: 600; color: #F4F5F7;">{dados_user['nome']}</div>
        <div style="font-size: 12px; color: #AEB6C2; margin-top: 2px;">{tipo_usuario_str}</div>
    </div>
""", unsafe_allow_html=True)

if st.sidebar.button("Encerrar sessão", type="secondary", use_container_width=True):
    st.session_state['usuario_logado'] = None
    st.rerun()

st.sidebar.markdown("---")

if is_admin:
    st.sidebar.markdown("<div style='font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600; color: #8F98A6; margin-bottom: 8px;'>Painel</div>", unsafe_allow_html=True)
    
    if st.sidebar.button("Gerenciar escritórios", type="secondary", use_container_width=True):
        st.session_state['modo_gerenciar'] = not st.session_state['modo_gerenciar']
        st.rerun()

    st.sidebar.markdown("---")
    lista_nomes_clientes = [u['nome'] for u in st.session_state['usuarios'].values() if u['tipo'] == 'cliente']
    if lista_nomes_clientes:
        st.sidebar.markdown("<div style='font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600; color: #8F98A6; margin-bottom: 6px;'>Escritório ativo</div>", unsafe_allow_html=True)
        escritorio_selecionado = st.sidebar.selectbox("Selecionar escritório ativo", lista_nomes_clientes, label_visibility="collapsed")
    else:
        escritorio_selecionado = "Nenhum"
else:
    escritorio_selecionado = dados_user['nome']
    if escritorio_selecionado not in st.session_state['base_dados_geral']:
        st.session_state['base_dados_geral'][escritorio_selecionado] = {}

st.sidebar.markdown("<div style='font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600; color: #8F98A6; margin-bottom: 8px;'>Período</div>", unsafe_allow_html=True)
meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
mes_escolhido = st.sidebar.selectbox("Mês", meses_do_ano, index=7)
ano_escolhido = st.sidebar.number_input("Ano", min_value=2024, max_value=2035, value=2026)
mes_ano_str = f"{mes_escolhido}/{ano_escolhido}"

semana_atual = st.sidebar.selectbox("Semana de Referência", ["Semana 1", "Semana 2", "Semana 3", "Semana 4"])

# --- CABEÇALHO PRINCIPAL INTEGRADO ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(f"""
        <div>
            <div style="font-size: 30px; font-weight: 600; color: #202632; letter-spacing: -0.03em; line-height: 1.1;">Muller Oliveira</div>
            <div style="font-size: 11px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: #7D8490; margin-top: 6px;">Controladoria & Gestão Executiva</div>
        </div>
    """, unsafe_allow_html=True)
with col_h2:
    st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E5E9; border-radius: 10px; padding: 10px 14px; text-align: right;">
            <div style="font-size: 9px; letter-spacing: 0.14em; text-transform: uppercase; color: #8C939F; margin-bottom: 2px;">Cliente Ativo</div>
            <div style="font-size: 14px; font-weight: 600; color: #202632;">{escritorio_selecionado}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

# --- MODO GERENCIAR ESCRITÓRIOS (ADMIN) ---
if is_admin and st.session_state.get('modo_gerenciar', False):
    st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E5E9; border-radius: 12px; padding: 24px; margin-bottom: 32px;">
            <h3 style="margin-top: 0; font-size: 20px;">Gestão de Escritórios Clientes</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2, gap="large")
    with col_g1:
        with st.form("cad_escritorio_main"):
            st.markdown("#### Cadastrar Novo Escritório")
            novo_id = st.text_input("Usuário de acesso", placeholder="escritorio_b")
            novo_nome = st.text_input("Nome do escritório", placeholder="Nayara Lira Advocacia")
            nova_senha = st.text_input("Senha", type="password")
            salvar_escritorio = st.form_submit_button("Criar acesso", type="primary", use_container_width=True)
            
            if salvar_escritorio:
                u_id_clean = novo_id.strip().lower()
                n_nome_clean = novo_nome.strip().upper()
                n_senha_clean = nova_senha.strip()
                if u_id_clean and n_nome_clean and n_senha_clean:
                    usuarios_atuais = carregar_usuarios()
                    usuarios_atuais[u_id_clean] = {"senha": n_senha_clean, "nome": n_nome_clean, "tipo": "cliente"}
                    salvar_usuarios(usuarios_atuais)
                    st.session_state['usuarios'] = usuarios_atuais
                    
                    if n_nome_clean not in st.session_state['base_dados_geral']:
                        st.session_state['base_dados_geral'][n_nome_clean] = {}
                    st.success(f"Escritório '{n_nome_clean}' (Usuário: {u_id_clean}) salvo permanentemente com sucesso!")
                else:
                    st.error("Preencha todos os campos corretamente.")

    with col_g2:
        with st.form("del_escritorio_main"):
            st.markdown("#### Remover Escritório")
            usuarios_atuais = carregar_usuarios()
            lista_clientes = [u['nome'] for u in usuarios_atuais.values() if u['tipo'] == 'cliente']
            if lista_clientes:
                escritorio_para_excluir = st.selectbox("Selecionar escritório para remoção", lista_clientes)
                excluir_btn = st.form_submit_button("Excluir escritório", use_container_width=True)
                if excluir_btn:
                    chave_del = [k for k, v in usuarios_atuais.items() if v['nome'] == escritorio_para_excluir]
                    if chave_del:
                        del usuarios_atuais[chave_del[0]]
                        salvar_usuarios(usuarios_atuais)
                        st.session_state['usuarios'] = usuarios_atuais
                    if escritorio_para_excluir in st.session_state['base_dados_geral']:
                        del st.session_state['base_dados_geral'][escritorio_para_excluir]
                    st.success(f"Escritório '{escritorio_para_excluir}' removido.")
                    st.rerun()
            else:
                st.info("Nenhum cliente cadastrado.")

    if st.button("← Voltar ao Dashboard Principal"):
        st.session_state['modo_gerenciar'] = False
        st.rerun()

elif escritorio_selecionado == "Nenhum":
    st.warning("Nenhum escritório cliente cadastrado. Utilize o botão 'Gerenciar escritórios' no menu lateral.")
else:
    if escritorio_selecionado not in st.session_state['base_dados_geral']:
        st.session_state['base_dados_geral'][escritorio_selecionado] = {}

    if mes_ano_str not in st.session_state['base_dados_geral'][escritorio_selecionado]:
        st.session_state['base_dados_geral'][escritorio_selecionado][mes_ano_str] = {
            "Semana 1": {}, "Semana 2": {}, "Semana 3": {}, "Semana 4": {}
        }

    historico_mes = st.session_state['base_dados_geral'][escritorio_selecionado][mes_ano_str]
    dados_semana_salvos = historico_mes.get(semana_atual, {})

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Lançamento", 
        "Consolidado", 
        "Previsibilidade", 
        "Diagnóstico", 
        "Plano de Ação"
    ])

    with tab1:
        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
            st.markdown(f"""
                <div style="margin-bottom: 28px;">
                    <h2 style="font-size: 30px; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 6px 0;">Lançamento semanal</h2>
                    <div style="font-size: 14px; font-weight: 400; color: #6E7684;"><span style="color: #202632; font-weight: 500;">{escritorio_selecionado}</span> · {mes_escolhido} de {ano_escolhido} · {semana_atual}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_t2:
            st.markdown("<div style='padding-top: 4px;'></div>", unsafe_allow_html=True)
            if st.button("Limpar semana", type="secondary"):
                st.session_state['base_dados_geral'][escritorio_selecionado][mes_ano_str][semana_atual] = {}
                st.success(f"Dados da {semana_atual} limpos.")
                st.rerun()

        # --- ABAS DE SETORES NO LANÇAMENTO SEMANAL ---
        sub_tab_com, sub_tab_adm, sub_tab_jud, sub_tab_fin, sub_tab_cs, sub_tab_eq = st.tabs([
            "1. Comercial", 
            "2. Administrativo", 
            "3. Judicial", 
            "4. Financeiro", 
            "5. Sucesso do Cliente", 
            "6. Equipe Ativa"
        ])

        with st.form(f"form_setores_{escritorio_selecionado}_{mes_ano_str}_{semana_atual}"):
            
            with sub_tab_com:
                st.markdown("#### Comercial (Físico & Digital)")
                leads = st.number_input("Quantidade de Leads", value=int(dados_semana_salvos.get('leads', 0)))
                leads_fisico = st.number_input("Atendimentos Comercial Físico", value=int(dados_semana_salvos.get('leads_fisico', 0)))
                leads_digital = st.number_input("Atendimentos Comercial Digital", value=int(dados_semana_salvos.get('leads_digital', 0)))
                qualificados = st.number_input("Contratos qualificados gerais", value=int(dados_semana_salvos.get('qualificados', 0)))
                contratos = st.number_input("Contratos fechados (Vendido)", value=int(dados_semana_salvos.get('contratos', 0)))
                receita_contratada = st.number_input("Receita contratada (R$)", value=float(dados_semana_salvos.get('receita_contratada', 0.0)))
                comercial_cancelados = st.number_input("Comercial: Quantidade de Cancelados / Desistências", value=int(dados_semana_salvos.get('comercial_cancelados', 0)))

            with sub_tab_adm:
                st.markdown("#### Operacional Administrativo (INSS) - Protocolos, Deferimentos e Indeferimentos")
                inss_geral = st.number_input("Protocolos Adm. INSS Totais", value=int(dados_semana_salvos.get('inss_geral', 0)))
                
                st.markdown("##### Detalhamento por Benefício (Adm)")
                
                col_a1, col_a2, col_a3 = st.columns(3)
                with col_a1:
                    inss_apos_idade = st.number_input("Aposentadoria por Idade (Prot)", value=int(dados_semana_salvos.get('inss_apos_idade', 0)))
                    inss_apos_idade_def = st.number_input("Aposentadoria por Idade (Def)", value=int(dados_semana_salvos.get('inss_apos_idade_def', 0)))
                    inss_apos_idade_ind = st.number_input("Aposentadoria por Idade (Ind)", value=int(dados_semana_salvos.get('inss_apos_idade_ind', 0)))
                with col_a2:
                    inss_apos_idade_rural = st.number_input("Apos. Idade Rural (Prot)", value=int(dados_semana_salvos.get('inss_apos_idade_rural', 0)))
                    inss_apos_idade_rural_def = st.number_input("Apos. Idade Rural (Def)", value=int(dados_semana_salvos.get('inss_apos_idade_rural_def', 0)))
                    inss_apos_idade_rural_ind = st.number_input("Apos. Idade Rural (Ind)", value=int(dados_semana_salvos.get('inss_apos_idade_rural_ind', 0)))
                with col_a3:
                    inss_apos_tempo = st.number_input("Apos. Tempo/Contrib. (Prot)", value=int(dados_semana_salvos.get('inss_apos_tempo', 0)))
                    inss_apos_tempo_def = st.number_input("Apos. Tempo/Contrib. (Def)", value=int(dados_semana_salvos.get('inss_apos_tempo_def', 0)))
                    inss_apos_tempo_ind = st.number_input("Apos. Tempo/Contrib. (Ind)", value=int(dados_semana_salvos.get('inss_apos_tempo_ind', 0)))

                col_b1, col_b2, col_b3 = st.columns(3)
                with col_b1:
                    inss_invalidez = st.number_input("Apos. Invalidez (Prot)", value=int(dados_semana_salvos.get('inss_invalidez', 0)))
                    inss_invalidez_def = st.number_input("Apos. Invalidez (Def)", value=int(dados_semana_salvos.get('inss_invalidez_def', 0)))
                    inss_invalidez_ind = st.number_input("Apos. Invalidez (Ind)", value=int(dados_semana_salvos.get('inss_invalidez_ind', 0)))
                with col_b2:
                    inss_pensao = st.number_input("Pensão por Morte (Prot)", value=int(dados_semana_salvos.get('inss_pensao', 0)))
                    inss_pensao_def = st.number_input("Pensão por Morte (Def)", value=int(dados_semana_salvos.get('inss_pensao_def', 0)))
                    inss_pensao_ind = st.number_input("Pensão por Morte (Ind)", value=int(dados_semana_salvos.get('inss_pensao_ind', 0)))
                with col_b3:
                    inss_aux_doenca = st.number_input("Auxílio Doença (Prot)", value=int(dados_semana_salvos.get('inss_aux_doenca', 0)))
                    inss_aux_doenca_def = st.number_input("Auxílio Doença (Def)", value=int(dados_semana_salvos.get('inss_aux_doenca_def', 0)))
                    inss_aux_doenca_ind = st.number_input("Auxílio Doença (Ind)", value=int(dados_semana_salvos.get('inss_aux_doenca_ind', 0)))

                col_c1, col_c2, col_c3 = st.columns(3)
                with col_c1:
                    inss_incapacidade_rural = st.number_input("Incapacidade Rural (Prot)", value=int(dados_semana_salvos.get('inss_incapacidade_rural', 0)))
                    inss_incapacidade_rural_def = st.number_input("Incapacidade Rural (Def)", value=int(dados_semana_salvos.get('inss_incapacidade_rural_def', 0)))
                    inss_incapacidade_rural_ind = st.number_input("Incapacidade Rural (Ind)", value=int(dados_semana_salvos.get('inss_incapacidade_rural_ind', 0)))
                with col_c2:
                    inss_sal_maternidade = st.number_input("Salário Maternidade (Prot)", value=int(dados_semana_salvos.get('inss_sal_maternidade', 0)))
                    inss_sal_maternidade_def = st.number_input("Salário Maternidade (Def)", value=int(dados_semana_salvos.get('inss_sal_maternidade_def', 0)))
                    inss_sal_maternidade_ind = st.number_input("Salário Maternidade (Ind)", value=int(dados_semana_salvos.get('inss_sal_maternidade_ind', 0)))
                with col_c3:
                    inss_aux_acidente = st.number_input("Auxílio-Acidente (Prot)", value=int(dados_semana_salvos.get('inss_aux_acidente', 0)))
                    inss_aux_acidente_def = st.number_input("Auxílio-Acidente (Def)", value=int(dados_semana_salvos.get('inss_aux_acidente_def', 0)))
                    inss_aux_acidente_ind = st.number_input("Auxílio-Acidente (Ind)", value=int(dados_semana_salvos.get('inss_aux_acidente_ind', 0)))

                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    inss_bpc_idoso = st.number_input("BPC Idoso (Prot)", value=int(dados_semana_salvos.get('inss_bpc_idoso', 0)))
                    inss_bpc_idoso_def = st.number_input("BPC Idoso (Def)", value=int(dados_semana_salvos.get('inss_bpc_idoso_def', 0)))
                    inss_bpc_idoso_ind = st.number_input("BPC Idoso (Ind)", value=int(dados_semana_salvos.get('inss_bpc_idoso_ind', 0)))
                with col_d2:
                    inss_bpc_deficiente = st.number_input("BPC Deficiente (Prot)", value=int(dados_semana_salvos.get('inss_bpc_deficiente', 0)))
                    inss_bpc_deficiente_def = st.number_input("BPC Deficiente (Def)", value=int(dados_semana_salvos.get('inss_bpc_deficiente_def', 0)))
                    inss_bpc_deficiente_ind = st.number_input("BPC Deficiente (Ind)", value=int(dados_semana_salvos.get('inss_bpc_deficiente_ind', 0)))

                st.markdown("##### Perícias, Exigências & Encaminhamentos (Adm)")
                adm_pericia_agendada = st.number_input("Adm: Perícias agendadas", value=int(dados_semana_salvos.get('adm_pericia_agendada', 0)))
                adm_pericia_realizada = st.number_input("Adm: Perícias realizadas", value=int(dados_semana_salvos.get('adm_pericia_realizada', 0)))
                adm_pericia_ausencia = st.number_input("Adm: Ausências em perícias", value=int(dados_semana_salvos.get('adm_pericia_ausencia', 0)))
                adm_pericia_reagendada = st.number_input("Adm: Perícias reagendadas/remarcadas", value=int(dados_semana_salvos.get('adm_pericia_reagendada', 0)))
                
                adm_av_soc_agendada = st.number_input("Adm: Avaliação social agendada", value=int(dados_semana_salvos.get('adm_av_soc_agendada', 0)))
                adm_av_soc_realizada = st.number_input("Adm: Avaliação social realizada", value=int(dados_semana_salvos.get('adm_av_soc_realizada', 0)))
                adm_av_soc_ausencia = st.number_input("Adm: Avaliação social - ausências", value=int(dados_semana_salvos.get('adm_av_soc_ausencia', 0)))
                adm_av_soc_reagendada = st.number_input("Adm: Avaliação social reagendada/remarcada", value=int(dados_semana_salvos.get('adm_av_soc_reagendada', 0)))
                
                adm_exig_cumprir = st.number_input("Adm: Quantidade de exigências a cumprir", value=int(dados_semana_salvos.get('adm_exig_cumprir', 0)))
                adm_exig_cumpridas = st.number_input("Adm: Quantidade de exigências cumpridas", value=int(dados_semana_salvos.get('adm_exig_cumpridas', 0)))
                
                adm_enviados_judicial = st.number_input("Adm: Enviados ao Judicial", value=int(dados_semana_salvos.get('adm_enviados_judicial', 0)))
                adm_retrabalho = st.number_input("Adm: Retrabalho/Reprotocolo", value=int(dados_semana_salvos.get('adm_retrabalho', 0)))
                adm_cancelados = st.number_input("Adm: Quantidade de Cancelados / Desistências", value=int(dados_semana_salvos.get('adm_cancelados', 0)))

            with sub_tab_jud:
                st.markdown("#### Operacional Judicial - Protocolos, Deferimentos e Indeferimentos")
                judicial_iniciais = st.number_input("Protocolos Iniciais Judiciais Totais", value=int(dados_semana_salvos.get('judicial_iniciais', 0)))
                
                st.markdown("##### Detalhamento por Benefício (Judicial)")
                
                col_j1, col_j2, col_j3 = st.columns(3)
                with col_j1:
                    judicial_apos_idade = st.number_input("Judicial: Apos. Idade (Prot)", value=int(dados_semana_salvos.get('judicial_apos_idade', 0)))
                    judicial_apos_idade_def = st.number_input("Judicial: Apos. Idade (Def)", value=int(dados_semana_salvos.get('judicial_apos_idade_def', 0)))
                    judicial_apos_idade_ind = st.number_input("Judicial: Apos. Idade (Ind)", value=int(dados_semana_salvos.get('judicial_apos_idade_ind', 0)))
                with col_j2:
                    judicial_apos_idade_rural = st.number_input("Judicial: Apos. Idade Rural (Prot)", value=int(dados_semana_salvos.get('judicial_apos_idade_rural', 0)))
                    judicial_apos_idade_rural_def = st.number_input("Judicial: Apos. Idade Rural (Def)", value=int(dados_semana_salvos.get('judicial_apos_idade_rural_def', 0)))
                    judicial_apos_idade_rural_ind = st.number_input("Judicial: Apos. Idade Rural (Ind)", value=int(dados_semana_salvos.get('judicial_apos_idade_rural_ind', 0)))
                with col_j3:
                    judicial_apos_tempo = st.number_input("Judicial: Apos. Tempo (Prot)", value=int(dados_semana_salvos.get('judicial_apos_tempo', 0)))
                    judicial_apos_tempo_def = st.number_input("Judicial: Apos. Tempo (Def)", value=int(dados_semana_salvos.get('judicial_apos_tempo_def', 0)))
                    judicial_apos_tempo_ind = st.number_input("Judicial: Apos. Tempo (Ind)", value=int(dados_semana_salvos.get('judicial_apos_tempo_ind', 0)))

                col_k1, col_k2, col_k3 = st.columns(3)
                with col_k1:
                    judicial_invalidez = st.number_input("Judicial: Invalidez (Prot)", value=int(dados_semana_salvos.get('judicial_invalidez', 0)))
                    judicial_invalidez_def = st.number_input("Judicial: Invalidez (Def)", value=int(dados_semana_salvos.get('judicial_invalidez_def', 0)))
                    judicial_invalidez_ind = st.number_input("Judicial: Invalidez (Ind)", value=int(dados_semana_salvos.get('judicial_invalidez_ind', 0)))
                with col_k2:
                    judicial_pensao = st.number_input("Judicial: Pensão por Morte (Prot)", value=int(dados_semana_salvos.get('judicial_pensao', 0)))
                    judicial_pensao_def = st.number_input("Judicial: Pensão por Morte (Def)", value=int(dados_semana_salvos.get('judicial_pensao_def', 0)))
                    judicial_pensao_ind = st.number_input("Judicial: Pensão por Morte (Ind)", value=int(dados_semana_salvos.get('judicial_pensao_ind', 0)))
                with col_k3:
                    judicial_incapacidade_rural = st.number_input("Judicial: Incapacidade Rural (Prot)", value=int(dados_semana_salvos.get('judicial_incapacidade_rural', 0)))
                    judicial_incapacidade_rural_def = st.number_input("Judicial: Incapacidade Rural (Def)", value=int(dados_semana_salvos.get('judicial_incapacidade_rural_def', 0)))
                    judicial_incapacidade_rural_ind = st.number_input("Judicial: Incapacidade Rural (Ind)", value=int(dados_semana_salvos.get('judicial_incapacidade_rural_ind', 0)))

                col_l1, col_l2 = st.columns(2)
                with col_l1:
                    judicial_bpc_idoso = st.number_input("Judicial: BPC Idoso (Prot)", value=int(dados_semana_salvos.get('judicial_bpc_idoso', 0)))
                    judicial_bpc_idoso_def = st.number_input("Judicial: BPC Idoso (Def)", value=int(dados_semana_salvos.get('judicial_bpc_idoso_def', 0)))
                    judicial_bpc_idoso_ind = st.number_input("Judicial: BPC Idoso (Ind)", value=int(dados_semana_salvos.get('judicial_bpc_idoso_ind', 0)))
                with col_l2:
                    judicial_bpc_deficiente = st.number_input("Judicial: BPC Deficiente (Prot)", value=int(dados_semana_salvos.get('judicial_bpc_deficiente', 0)))
                    judicial_bpc_deficiente_def = st.number_input("Judicial: BPC Deficiente (Def)", value=int(dados_semana_salvos.get('judicial_bpc_deficiente_def', 0)))
                    judicial_bpc_deficiente_ind = st.number_input("Judicial: BPC Deficiente (Ind)", value=int(dados_semana_salvos.get('judicial_bpc_deficiente_ind', 0)))

                judicial_emendas = st.number_input("Judicial: Emendas às iniciais", value=int(dados_semana_salvos.get('judicial_emendas', 0)))
                judicial_pericia_agendada = st.number_input("Judicial: Perícias agendadas", value=int(dados_semana_salvos.get('judicial_pericia_agendada', 0)))
                judicial_pericia_realizada = st.number_input("Judicial: Perícias realizadas", value=int(dados_semana_salvos.get('judicial_pericia_realizada', 0)))
                judicial_pericia_ausencia = st.number_input("Judicial: Ausências em perícias", value=int(dados_semana_salvos.get('judicial_pericia_ausencia', 0)))
                judicial_recursos = st.number_input("Judicial: Recursos", value=int(dados_semana_salvos.get('judicial_recursos', 0)))
                judicial_rec_providos = st.number_input("Judicial: Recursos providos", value=int(dados_semana_salvos.get('judicial_rec_providos', 0)))
                judicial_rec_improvidos = st.number_input("Judicial: Recursos improvidos", value=int(dados_semana_salvos.get('judicial_rec_improvidos', 0)))
                
                sentecas_proc = st.number_input("Sentenças procedentes", value=int(dados_semana_salvos.get('sentecas_proc', 0)))
                sentecas_improc = st.number_input("Sentenças improcedentes", value=int(dados_semana_salvos.get('sentecas_improc', 0)))
                judicial_extinto = st.number_input("Judicial: Extinto sem resolução", value=int(dados_semana_salvos.get('judicial_extinto', 0)))
                judicial_estoque = st.number_input("Judicial: Estoque (em revisão/aguardando protocolo)", value=int(dados_semana_salvos.get('judicial_estoque', 0)))
                judicial_retrabalho = st.number_input("Judicial: Retrabalho/Reprotocolo", value=int(dados_semana_salvos.get('judicial_retrabalho', 0)))
                judicial_cancelados = st.number_input("Judicial: Quantidade de Cancelados / Desistências", value=int(dados_semana_salvos.get('judicial_cancelados', 0)))
                
                prazos_fatal = st.number_input("Prazos protocolados no fatal", value=int(dados_semana_salvos.get('prazos_fatal', 0)))
                prazos_perdidos = st.number_input("Prazos perdidos", value=int(dados_semana_salvos.get('prazos_perdidos', 0)))
                acordos_homologados = st.number_input("Acordos homologados", value=int(dados_semana_salvos.get('acordos_homologados', 0)))

            with sub_tab_fin:
                st.markdown("#### Financeiro")
                faturamento = st.number_input("Faturamento emitido (R$)", value=float(dados_semana_salvos.get('faturamento', 0.0)))
                recebido = st.number_input("Valor efetivamente recebido (R$)", value=float(dados_semana_salvos.get('recebido', 0.0)))
                vencido = st.number_input("Valor vencido / inadimplente (R$)", value=float(dados_semana_salvos.get('vencido', 0.0)))
                rpv_precatorio = st.number_input("RPV / Precatório recebidos (R$)", value=float(dados_semana_salvos.get('rpv_precatorio', 0.0)))
                pagamento_adm = st.number_input("Pagamento Administrativo (R$)", value=float(dados_semana_salvos.get('pagamento_adm', 0.0)))

            with sub_tab_cs:
                st.markdown("#### Sucesso do Cliente & Controladoria")
                cs_contatos = st.number_input("Contatos de relacionamento CS", value=int(dados_semana_salvos.get('cs_contatos', 0)))
                nps = st.number_input("NPS (Net Promoter Score)", value=float(dados_semana_salvos.get('nps', 0.0)))
                contatos_aniversariantes = st.number_input("Contatos com aniversariantes do dia", value=int(dados_semana_salvos.get('contatos_aniversariantes', 0)))
                processos_arquivados = st.number_input("Processos arquivados", value=int(dados_semana_salvos.get('processos_arquivados', 0)))
                clientes_aguard_judicial = st.number_input("Clientes aguardando envio Judicial", value=int(dados_semana_salvos.get('clientes_aguard_judicial', 0)))
                clientes_aguard_adm = st.number_input("Clientes aguardando envio Administrativo", value=int(dados_semana_salvos.get('clientes_aguard_adm', 0)))
                avaliacoes_google = st.number_input("Novas avaliações no Google", value=int(dados_semana_salvos.get('avaliacoes_google', 0)))
                cancelados_desistencia = st.number_input("Cancelados por Desistência (Geral CS)", value=int(dados_semana_salvos.get('cancelados_desistencia', 0)))
                cancelados_docs_direito = st.number_input("Cancelados - Docs/Direito", value=int(dados_semana_salvos.get('cancelados_docs_direito', 0)))

            with sub_tab_eq:
                st.markdown("#### Equipe Ativa por Área")
                eq_comercial = st.number_input("Equipe: Comercial", value=int(dados_semana_salvos.get('eq_comercial', 0)))
                eq_financeiro = st.number_input("Equipe: Financeiro", value=int(dados_semana_salvos.get('eq_financeiro', 0)))
                eq_cs = st.number_input("Equipe: Sucesso do Cliente & Controladoria", value=int(dados_semana_salvos.get('eq_cs', 0)))
                eq_adm = st.number_input("Equipe: Operacional Administrativo (INSS)", value=int(dados_semana_salvos.get('eq_adm', 0)))
                eq_judicial = st.number_input("Equipe: Operacional Judicial", value=int(dados_semana_salvos.get('eq_judicial', 0)))

            st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)
            if submitted:
                st.session_state['base_dados_geral'][escritorio_selecionado][mes_ano_str][semana_atual] = {
                    'leads': leads, 'leads_fisico': leads_fisico, 'leads_digital': leads_digital, 'qualificados': qualificados, 'contratos': contratos, 'receita_contratada': receita_contratada, 'comercial_cancelados': comercial_cancelados,
                    'inss_geral': inss_geral, 
                    'inss_apos_idade': inss_apos_idade, 'inss_apos_idade_def': inss_apos_idade_def, 'inss_apos_idade_ind': inss_apos_idade_ind,
                    'inss_apos_idade_rural': inss_apos_idade_rural, 'inss_apos_idade_rural_def': inss_apos_idade_rural_def, 'inss_apos_idade_rural_ind': inss_apos_idade_rural_ind,
                    'inss_apos_tempo': inss_apos_tempo, 'inss_apos_tempo_def': inss_apos_tempo_def, 'inss_apos_tempo_ind': inss_apos_tempo_ind,
                    'inss_invalidez': inss_invalidez, 'inss_invalidez_def': inss_invalidez_def, 'inss_invalidez_ind': inss_invalidez_ind,
                    'inss_pensao': inss_pensao, 'inss_pensao_def': inss_pensao_def, 'inss_pensao_ind': inss_pensao_ind,
                    'inss_aux_doenca': inss_aux_doenca, 'inss_aux_doenca_def': inss_aux_doenca_def, 'inss_aux_doenca_ind': inss_aux_doenca_ind,
                    'inss_incapacidade_rural': inss_incapacidade_rural, 'inss_incapacidade_rural_def': inss_incapacidade_rural_def, 'inss_incapacidade_rural_ind': inss_incapacidade_rural_ind,
                    'inss_sal_maternidade': inss_sal_maternidade, 'inss_sal_maternidade_def': inss_sal_maternidade_def, 'inss_sal_maternidade_ind': inss_sal_maternidade_ind,
                    'inss_aux_acidente': inss_aux_acidente, 'inss_aux_acidente_def': inss_aux_acidente_def, 'inss_aux_acidente_ind': inss_aux_acidente_ind,
                    'inss_bpc_idoso': inss_bpc_idoso, 'inss_bpc_idoso_def': inss_bpc_idoso_def, 'inss_bpc_idoso_ind': inss_bpc_idoso_ind,
                    'inss_bpc_deficiente': inss_bpc_deficiente, 'inss_bpc_deficiente_def': inss_bpc_deficiente_def, 'inss_bpc_deficiente_ind': inss_bpc_deficiente_ind,
                    'adm_pericia_agendada': adm_pericia_agendada, 'adm_pericia_realizada': adm_pericia_realizada, 'adm_pericia_ausencia': adm_pericia_ausencia, 'adm_pericia_reagendada': adm_pericia_reagendada,
                    'adm_av_soc_agendada': adm_av_soc_agendada, 'adm_av_soc_realizada': adm_av_soc_realizada, 'adm_av_soc_ausencia': adm_av_soc_ausencia, 'adm_av_soc_reagendada': adm_av_soc_reagendada,
                    'adm_exig_cumprir': adm_exig_cumprir, 'adm_exig_cumpridas': adm_exig_cumpridas, 'adm_enviados_judicial': adm_enviados_judicial, 'adm_retrabalho': adm_retrabalho, 'adm_cancelados': adm_cancelados,
                    'judicial_iniciais': judicial_iniciais, 
                    'judicial_apos_idade': judicial_apos_idade, 'judicial_apos_idade_def': judicial_apos_idade_def, 'judicial_apos_idade_ind': judicial_apos_idade_ind,
                    'judicial_apos_idade_rural': judicial_apos_idade_rural, 'judicial_apos_idade_rural_def': judicial_apos_idade_rural_def, 'judicial_apos_idade_rural_ind': judicial_apos_idade_rural_ind,
                    'judicial_apos_tempo': judicial_apos_tempo, 'judicial_apos_tempo_def': judicial_apos_tempo_def, 'judicial_apos_tempo_ind': judicial_apos_tempo_ind,
                    'judicial_invalidez': judicial_invalidez, 'judicial_invalidez_def': judicial_invalidez_def, 'judicial_invalidez_ind': judicial_invalidez_ind,
                    'judicial_pensao': judicial_pensao, 'judicial_pensao_def': judicial_pensao_def, 'judicial_pensao_ind': judicial_pensao_ind,
                    'judicial_incapacidade_rural': judicial_incapacidade_rural, 'judicial_incapacidade_rural_def': judicial_incapacidade_rural_def, 'judicial_incapacidade_rural_ind': judicial_incapacidade_rural_ind,
                    'judicial_bpc_idoso': judicial_bpc_idoso, 'judicial_bpc_idoso_def': judicial_bpc_idoso_def, 'judicial_bpc_idoso_ind': judicial_bpc_idoso_ind,
                    'judicial_bpc_deficiente': judicial_bpc_deficiente, 'judicial_bpc_deficiente_def': judicial_bpc_deficiente_def, 'judicial_bpc_deficiente_ind': judicial_bpc_deficiente_ind,
                    'judicial_emendas': judicial_emendas, 'judicial_pericia_agendada': judicial_pericia_agendada, 'judicial_pericia_realizada': judicial_pericia_realizada, 'judicial_pericia_ausencia': judicial_pericia_ausencia,
                    'judicial_recursos': judicial_recursos, 'judicial_rec_providos': judicial_rec_providos, 'judicial_rec_improvidos': judicial_rec_improvidos,
                    'sentecas_proc': sentecas_proc, 'sentecas_improc': sentecas_improc, 'judicial_extinto': judicial_extinto, 'judicial_estoque': judicial_estoque, 'judicial_retrabalho': judicial_retrabalho, 'judicial_cancelados': judicial_cancelados,
                    'prazos_fatal': prazos_fatal, 'prazos_perdidos': prazos_perdidos, 'acordos_homologados': acordos_homologados,
                    'faturamento': faturamento, 'recebido': recebido, 'vencido': vencido, 'rpv_precatorio': rpv_precatorio, 'pagamento_adm': pagamento_adm, 
                    'cs_contatos': cs_contatos, 'nps': nps, 'contatos_aniversariantes': contatos_aniversariantes, 'processos_arquivados': processos_arquivados,
                    'clientes_aguard_judicial': clientes_aguard_judicial, 'clientes_aguard_adm': clientes_aguard_adm, 'avaliacoes_google': avaliacoes_google, 
                    'cancelados_desistencia': cancelados_desistencia, 'cancelados_docs_direito': cancelados_docs_direito,
                    'eq_comercial': eq_comercial, 'eq_financeiro': eq_financeiro, 'eq_cs': eq_cs, 'eq_adm': eq_adm, 'eq_judicial': eq_judicial
                }
                st.success(f"Dados da **{semana_atual}** salvos com sucesso.")
                st.rerun()

    # --- CONSOLIDAÇÃO MENSAL COMPLETA ---
    totais_mes = {}
    chaves_numericas = [
        'leads', 'leads_fisico', 'leads_digital', 'qualificados', 'contratos', 'receita_contratada', 'comercial_cancelados',
        'inss_geral', 'inss_apos_idade', 'inss_apos_idade_def', 'inss_apos_idade_ind', 'inss_apos_idade_rural', 'inss_apos_idade_rural_def', 'inss_apos_idade_rural_ind',
        'inss_apos_tempo', 'inss_apos_tempo_def', 'inss_apos_tempo_ind', 'inss_invalidez', 'inss_invalidez_def', 'inss_invalidez_ind',
        'inss_pensao', 'inss_pensao_def', 'inss_pensao_ind', 'inss_aux_doenca', 'inss_aux_doenca_def', 'inss_aux_doenca_ind', 
        'inss_incapacidade_rural', 'inss_incapacidade_rural_def', 'inss_incapacidade_rural_ind', 'inss_sal_maternidade', 'inss_sal_maternidade_def', 'inss_sal_maternidade_ind',
        'inss_aux_acidente', 'inss_aux_acidente_def', 'inss_aux_acidente_ind', 'inss_bpc_idoso', 'inss_bpc_idoso_def', 'inss_bpc_idoso_ind',
        'inss_bpc_deficiente', 'inss_bpc_deficiente_def', 'inss_bpc_deficiente_ind',
        'adm_pericia_agendada', 'adm_pericia_realizada', 'adm_pericia_ausencia', 'adm_pericia_reagendada',
        'adm_av_soc_agendada', 'adm_av_soc_realizada', 'adm_av_soc_ausencia', 'adm_av_soc_reagendada',
        'adm_exig_cumprir', 'adm_exig_cumpridas', 'adm_enviados_judicial', 'adm_retrabalho', 'adm_cancelados',
        'judicial_iniciais', 'judicial_apos_idade', 'judicial_apos_idade_def', 'judicial_apos_idade_ind',
        'judicial_apos_idade_rural', 'judicial_apos_idade_rural_def', 'judicial_apos_idade_rural_ind',
        'judicial_apos_tempo', 'judicial_apos_tempo_def', 'judicial_apos_tempo_ind', 'judicial_invalidez', 'judicial_invalidez_def', 'judicial_invalidez_ind',
        'judicial_pensao', 'judicial_pensao_def', 'judicial_pensao_ind', 'judicial_sal_maternidade', 'judicial_sal_maternidade_def', 'judicial_sal_maternidade_ind',
        'judicial_aux_acidente', 'judicial_incapacidade_rural', 'judicial_incapacidade_rural_def', 'judicial_incapacidade_rural_ind',
        'judicial_bpc_idoso', 'judicial_bpc_idoso_def', 'judicial_bpc_idoso_ind', 'judicial_bpc_deficiente', 'judicial_bpc_deficiente_def', 'judicial_bpc_deficiente_ind',
        'judicial_emendas', 'judicial_pericia_agendada', 'judicial_pericia_realizada', 'judicial_pericia_ausencia',
        'judicial_recursos', 'judicial_rec_providos', 'judicial_rec_improvidos',
        'sentecas_proc', 'sentecas_improc', 'judicial_extinto', 'judicial_estoque', 'judicial_retrabalho', 'judicial_cancelados',
        'prazos_fatal', 'prazos_perdidos', 'acordos_homologados', 'faturamento', 'recebido', 'vencido', 'rpv_precatorio', 'pagamento_adm', 
        'cs_contatos', 'nps', 'contatos_aniversariantes', 'processos_arquivados',
        'clientes_aguard_judicial', 'clientes_aguard_adm', 'avaliacoes_google', 
        'cancelados_desistencia', 'cancelados_docs_direito',
        'eq_comercial', 'eq_financeiro', 'eq_cs', 'eq_adm', 'eq_judicial'
    ]

    for chave in chaves_numericas:
        if chave == 'nps':
            vals = [semana.get(chave, 0.0) for semana in historico_mes.values() if semana.get(chave, 0.0) > 0]
            totais_mes[chave] = sum(vals) / len(vals) if vals else 0.0
        else:
            totais_mes[chave] = sum([semana.get(chave, 0) for semana in historico_mes.values()])

    taxa_conversao = (totais_mes['contratos'] / totais_mes['qualificados'] * 100) if totais_mes['qualificados'] > 0 else 0
    inadimplencia_pct = (totais_mes['vencido'] / totais_mes['faturamento'] * 100) if totais_mes['faturamento'] > 0 else 0
    total_aguardando = totais_mes['clientes_aguard_judicial'] + totais_mes['clientes_aguard_adm']
    total_entregue_protocolos = totais_mes['inss_geral'] + totais_mes['judicial_iniciais']

    if totais_mes['contratos'] == 0 and totais_mes['faturamento'] == 0:
        score_geral = 0.0
    else:
        score_comercial = 84.0 if taxa_conversao >= 20 else 60.0
        score_financeiro = 68.0 if inadimplencia_pct < 10 else 50.0
        score_operacao = 70.0
        score_cliente = 78.0 if totais_mes['avaliacoes_google'] >= 5 else 60.0
        score_gestao = 74.0
        score_geral = (score_comercial * 0.20) + (score_financeiro * 0.20) + (score_operacao * 0.30) + (score_cliente * 0.15) + (score_gestao * 0.15)

    with tab2:
        st.markdown(f"""
            <div style="margin-bottom: 28px;">
                <h2 style="font-size: 30px; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 6px 0;">Consolidado mensal</h2>
                <div style="font-size: 14px; font-weight: 400; color: #6E7684;"><span style="color: #202632; font-weight: 500;">{escritorio_selecionado}</span> · {mes_escolhido} de {ano_escolhido}</div>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4, gap="medium")
        status_score = "Aguardando dados" if score_geral == 0 else "Consolidado"
        c1.metric("Score de Gestão", f"{score_geral:.0f} / 100", status_score)
        c2.metric("Total Vendido", totais_mes['contratos'])
        c3.metric("Faturamento", f"R$ {totais_mes['faturamento']:,.2f}")
        c4.metric("Recebido Efetivo", f"R$ {totais_mes['recebido']:,.2f}")

        st.markdown("<div style='margin: 28px 0;'></div>", unsafe_allow_html=True)
        st.markdown("#### Comercial & Leads")
        f1, f2, f3, f4 = st.columns(4, gap="medium")
        f1.metric("Total Leads", totais_mes['leads'])
        f2.metric("Taxa de Conversão", f"{taxa_conversao:.1f}%")
        f3.metric("Receita Contratada", f"R$ {totais_mes['receita_contratada']:,.2f}")
        f4.metric("Cancelados / Desistências", totais_mes['comercial_cancelados'])

        st.markdown("<div style='margin: 28px 0;'></div>", unsafe_allow_html=True)
        st.markdown("#### Produção Operacional Consolidada (Adm & Judicial)")
        op1, op2, op3, op4 = st.columns(4, gap="medium")
        op1.metric("Protocolos INSS", totais_mes['inss_geral'])
        op2.metric("Protocolos Judiciais", totais_mes['judicial_iniciais'])
        op3.metric("Sentenças Procedentes", totais_mes['sentecas_proc'])
        op4.metric("Recursos Providos", totais_mes['judicial_rec_providos'])

        st.markdown("<div style='margin: 28px 0;'></div>", unsafe_allow_html=True)
        st.markdown("#### Sucesso do Cliente & Qualidade")
        sc1, sc2, sc3, sc4 = st.columns(4, gap="medium")
        sc1.metric("NPS Médio", f"{totais_mes['nps']:.1f}")
        sc2.metric("Aniversariantes Contatados", totais_mes['contatos_aniversariantes'])
        sc3.metric("Avaliações Google", totais_mes['avaliacoes_google'])
        sc4.metric("Processos Arquivados", totais_mes['processos_arquivados'])

        st.markdown("<div style='margin: 32px 0;'></div>", unsafe_allow_html=True)
        st.markdown("#### Histórico detalhado por semana")
        df_semanas = pd.DataFrame(historico_mes).T
        st.dataframe(df_semanas, use_container_width=True)

    with tab3:
        st.markdown(f"""
            <div style="margin-bottom: 28px;">
                <h2 style="font-size: 30px; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 6px 0;">Previsibilidade</h2>
                <div style="font-size: 14px; font-weight: 400; color: #6E7684;">Vendido x Entregue · <span style="color: #202632; font-weight: 500;">{escritorio_selecionado}</span></div>
            </div>
        """, unsafe_allow_html=True)
        
        col_p1, col_p2, col_p3 = st.columns(3, gap="medium")
        col_p1.metric("Total Vendido no Mês", totais_mes['contratos'])
        col_p2.metric("Total Entregue (INSS + Judicial)", total_entregue_protocolos, f"{totais_mes['inss_geral']} Adm / {totais_mes['judicial_iniciais']} Judicial")
        
        indice_vazao = (total_entregue_protocolos / totais_mes['contratos'] * 100) if totais_mes['contratos'] > 0 else 0
        col_p3.metric("Índice de Vazão", f"{indice_vazao:.1f}%", "Meta: 100%")

    with tab4:
        st.markdown(f"""
            <div style="margin-bottom: 28px;">
                <h2 style="font-size: 30px; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 6px 0;">Diagnóstico</h2>
                <div style="font-size: 14px; font-weight: 400; color: #6E7684;">Análise de estoques · <span style="color: #202632; font-weight: 500;">{escritorio_selecionado}</span></div>
            </div>
        """, unsafe_allow_html=True)
        
        if score_geral == 0:
            st.info("Preencha os dados das semanas para gerar o diagnóstico executivo.")
        else:
            st.error("Pontos de Atenção Operacional")
            st.write(f"Há **{total_aguardando} clientes** parados na esteira aguardando encaminhamento para o contencioso judicial ou administrativo.")

    with tab5:
        st.markdown(f"""
            <div style="margin-bottom: 28px;">
                <h2 style="font-size: 30px; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 6px 0;">Plano de ação</h2>
                <div style="font-size: 14px; font-weight: 400; color: #6E7684;">Diretrizes estratégicas · <span style="color: #202632; font-weight: 500;">{escritorio_selecionado}</span></div>
            </div>
        """, unsafe_allow_html=True)
        
        if score_geral == 0:
            st.info("Preencha os dados das semanas para gerar as diretrizes do plano de ação.")
        else:
            st.markdown(f"* **Foco Comercial:** Acelerar conversão digital e física frente aos {totais_mes['qualificados']} qualificados registrados no período.")
            st.markdown(f"* **Foco Retenção:** Tratar cancelamentos por desistência ({totais_mes['cancelados_desistencia']}) e docs/direito ({totais_mes['cancelados_docs_direito']}).")
