import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Controladoria & Gestão Executiva | Muller Oliveira", 
    page_icon="⚖️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

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

    /* Fundo Geral da Aplicação */
    .stApp {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Sidebar Executiva Escura */
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

    /* Ajuste para inputs dentro da Sidebar (texto legível) */
    section[data-testid="stSidebar"] div[data-baseweb="input"] input, 
    section[data-testid="stSidebar"] div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] .stNumberInput input, 
    section[data-testid="stSidebar"] .stTextInput input {
        color: #202632 !important;
    }

    /* Tipografia Global unificada em Inter */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text) !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }

    /* Inputs e Controles do Conteúdo Principal */
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

    /* Formulários e Superfícies */
    div[data-testid="stForm"] {
        background-color: var(--surface) !important;
        padding: 24px !important;
        border-radius: var(--radius-card) !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 1px 3px rgba(31, 38, 50, 0.04);
    }

    /* Cards de Métricas Compactos */
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

    /* Botões Primários (Champagne) */
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

    /* Botões Secundários */
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

    /* Navegação por Abas Minimalista */
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

# --- INICIALIZAÇÃO DE DADOS NO SESSION STATE ---
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {
        "admin": {"senha": "muller2026", "nome": "Muller Oliveira", "tipo": "admin"},
        "escritorio_a": {"senha": "123", "nome": "T.A. Advocacia", "tipo": "cliente"}
    }

if 'base_dados_geral' not in st.session_state:
    st.session_state['base_dados_geral'] = {
        "T.A. Advocacia": {}
    }

if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = None

# --- TELA DE AUTENTICAÇÃO EXECUTIVA (TEMA CLARO) ---
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
                    if usuario_input in st.session_state['usuarios'] and st.session_state['usuarios'][usuario_input]['senha'] == senha_input:
                        st.session_state['usuario_logado'] = usuario_input
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas.")
                        
        with aba_rec:
            st.markdown("<p style='font-size: 13px; color: #6E7684; margin-top: 10px;'>Solicite o reestabelecimento ao administrador.</p>", unsafe_allow_html=True)
            user_rec = st.text_input("Usuário cadastrado", key="rec_user")
            if st.button("Enviar solicitação", type="secondary", use_container_width=True):
                if user_rec in st.session_state['usuarios']:
                    st.success("Solicitação enviada com sucesso.")
                else:
                    st.warning("Usuário não localizado.")
    st.stop()

# --- SESSÃO ATIVA & SIDEBAR ORGANIZADA ---
user_atual = st.session_state['usuario_logado']
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
    
    with st.sidebar.expander("Gerenciar escritórios", expanded=False):
        with st.form("cad_escritorio"):
            st.markdown("**Novo Escritório**")
            novo_id = st.text_input("Usuário de acesso", placeholder="escritorio_b")
            novo_nome = st.text_input("Nome do escritório", placeholder="Nayara Lira Advocacia")
            nova_senha = st.text_input("Senha", type="password")
            salvar_escritorio = st.form_submit_button("Criar acesso", type="primary", use_container_width=True)
            
            if salvar_escritorio:
                if novo_id and novo_nome and nova_senha:
                    st.session_state['usuarios'][novo_id] = {"senha": nova_senha, "nome": novo_nome, "tipo": "cliente"}
                    if novo_nome not in st.session_state['base_dados_geral']:
                        st.session_state['base_dados_geral'][novo_nome] = {}
                    st.success(f"Escritório '{novo_nome}' criado.")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos.")

        st.markdown("---")
        lista_clientes = [u['nome'] for u in st.session_state['usuarios'].values() if u['tipo'] == 'cliente']
        if lista_clientes:
            escritorio_para_excluir = st.selectbox("Remover escritório", lista_clientes, key="del_esc")
            if st.button("Excluir escritório", type="secondary", use_container_width=True):
                chave_del = [k for k, v in st.session_state['usuarios'].items() if v['nome'] == escritorio_para_excluir]
                if chave_del:
                    del st.session_state['usuarios'][chave_del[0]]
                if escritorio_para_excluir in st.session_state['base_dados_geral']:
                    del st.session_state['base_dados_geral'][escritorio_para_excluir]
                st.success("Removido com sucesso.")
                st.rerun()
        else:
            st.info("Nenhum cliente cadastrado.")

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

# --- CABEÇALHO PRINCIPAL INTEGRADO (TEMA CLARO) ---
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

if escritorio_selecionado == "Nenhum":
    st.warning("Nenhum escritório cliente cadastrado. Utilize o painel lateral do consultor para cadastrar o primeiro cliente.")
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

        with st.form(f"form_{escritorio_selecionado}_{mes_ano_str}_{semana_atual}"):
            col1, col2 = st.columns(2, gap="large")
            with col1:
                st.markdown("#### Comercial (Físico & Digital)")
                leads_fisico = st.number_input("Atendimentos Comercial Físico", value=int(dados_semana_salvos.get('leads_fisico', 0)))
                leads_digital = st.number_input("Atendimentos Comercial Digital", value=int(dados_semana_salvos.get('leads_digital', 0)))
                qualificados = st.number_input("Contratos qualificados gerais", value=int(dados_semana_salvos.get('qualificados', 0)))
                contratos = st.number_input("Contratos fechados (Vendido)", value=int(dados_semana_salvos.get('contratos', 0)))
                receita_contratada = st.number_input("Receita contratada (R$)", value=float(dados_semana_salvos.get('receita_contratada', 0.0)))
                
                st.markdown("#### Operacional INSS (Protocolos)")
                inss_geral = st.number_input("Protocolos Adm. INSS Totais", value=int(dados_semana_salvos.get('inss_geral', 0)))
                inss_apos_idade = st.number_input("INSS: Aposentadoria por Idade", value=int(dados_semana_salvos.get('inss_apos_idade', 0)))
                inss_apos_tempo = st.number_input("INSS: Aposentadoria por Tempo/Contribuição", value=int(dados_semana_salvos.get('inss_apos_tempo', 0)))
                inss_invalidez = st.number_input("INSS: Aposentadoria por Invalidez", value=int(dados_semana_salvos.get('inss_invalidez', 0)))
                inss_pensao = st.number_input("INSS: Pensão por Morte", value=int(dados_semana_salvos.get('inss_pensao', 0)))
                inss_aux_doenca = st.number_input("INSS: Auxílio Doença / Incapacidade", value=int(dados_semana_salvos.get('inss_aux_doenca', 0)))
                inss_bpc = st.number_input("INSS: BPC / Loas", value=int(dados_semana_salvos.get('inss_bpc', 0)))

                st.markdown("#### Financeiro")
                faturamento = st.number_input("Faturamento emitido (R$)", value=float(dados_semana_salvos.get('faturamento', 0.0)))
                recebido = st.number_input("Valor efetivamente recebido (R$)", value=float(dados_semana_salvos.get('recebido', 0.0)))
                vencido = st.number_input("Valor vencido / inadimplente (R$)", value=float(dados_semana_salvos.get('vencido', 0.0)))
                rpv_precatorio = st.number_input("RPV / Precatório recebidos (R$)", value=float(dados_semana_salvos.get('rpv_precatorio', 0.0)))
                pagamento_adm = st.number_input("Pagamento Administrativo (R$)", value=float(dados_semana_salvos.get('pagamento_adm', 0.0)))

            with col2:
                st.markdown("#### Operacional Justiça Federal (JF)")
                jf_iniciais = st.number_input("Protocolos Iniciais JF Totais", value=int(dados_semana_salvos.get('jf_iniciais', 0)))
                jf_apos_idade = st.number_input("JF: Aposentadoria por Idade", value=int(dados_semana_salvos.get('jf_apos_idade', 0)))
                jf_apos_tempo = st.number_input("JF: Aposentadoria por Tempo", value=int(dados_semana_salvos.get('jf_apos_tempo', 0)))
                jf_invalidez = st.number_input("JF: Aposentadoria por Invalidez", value=int(dados_semana_salvos.get('jf_invalidez', 0)))
                jf_bpc = st.number_input("JF: BPC / Loas", value=int(dados_semana_salvos.get('jf_bpc', 0)))
                sentecas_proc = st.number_input("Sentenças procedentes", value=int(dados_semana_salvos.get('sentecas_proc', 0)))
                sentecas_improc = st.number_input("Sentenças improcedentes", value=int(dados_semana_salvos.get('sentecas_improc', 0)))

                st.markdown("#### Sucesso do Cliente & Controladoria")
                cs_contatos = st.number_input("Contatos de relacionamento CS", value=int(dados_semana_salvos.get('cs_contatos', 0)))
                processos_arquivados = st.number_input("Processos arquivados", value=int(dados_semana_salvos.get('processos_arquivados', 0)))
                clientes_aguard_judicial = st.number_input("Clientes aguardando envio Judicial", value=int(dados_semana_salvos.get('clientes_aguard_judicial', 0)))
                clientes_aguard_adm = st.number_input("Clientes aguardando envio Administrativo", value=int(dados_semana_salvos.get('clientes_aguard_adm', 0)))

                st.markdown("#### RH & Qualidade")
                tarefas_rh = st.number_input("Tarefas de RH concluídas", value=int(dados_semana_salvos.get('tarefas_rh', 0)))
                onboardings = st.number_input("Onboardings concluídos", value=int(dados_semana_salvos.get('onboardings', 0)))
                avaliacoes_google = st.number_input("Novas avaliações no Google", value=int(dados_semana_salvos.get('avaliacoes_google', 0)))
                cancelados_desistencia = st.number_input("Cancelados por Desistência", value=int(dados_semana_salvos.get('cancelados_desistencia', 0)))
                cancelados_docs_direito = st.number_input("Cancelados - Docs/Direito", value=int(dados_semana_salvos.get('cancelados_docs_direito', 0)))
                
                st.markdown("#### Equipe Ativa")
                advogados = st.number_input("Advogados", value=int(dados_semana_salvos.get('advogados', 0)))
                estagiarios = st.number_input("Estagiários", value=int(dados_semana_salvos.get('estagiarios', 0)))
                auxiliares = st.number_input("Auxiliares", value=int(dados_semana_salvos.get('auxiliares', 0)))

            st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)
            if submitted:
                st.session_state['base_dados_geral'][escritorio_selecionado][mes_ano_str][semana_atual] = {
                    'leads_fisico': leads_fisico, 'leads_digital': leads_digital, 'qualificados': qualificados, 'contratos': contratos, 'receita_contratada': receita_contratada,
                    'inss_geral': inss_geral, 'inss_apos_idade': inss_apos_idade, 'inss_apos_tempo': inss_apos_tempo, 'inss_invalidez': inss_invalidez, 'inss_pensao': inss_pensao, 'inss_aux_doenca': inss_aux_doenca, 'inss_bpc': inss_bpc,
                    'jf_iniciais': jf_iniciais, 'jf_apos_idade': jf_apos_idade, 'jf_apos_tempo': jf_apos_tempo, 'jf_invalidez': jf_invalidez, 'jf_bpc': jf_bpc,
                    'sentecas_proc': sentecas_proc, 'sentecas_improc': sentecas_improc, 'faturamento': faturamento, 'recebido': recebido, 'vencido': vencido,
                    'rpv_precatorio': rpv_precatorio, 'pagamento_adm': pagamento_adm, 'cs_contatos': cs_contatos, 'processos_arquivados': processos_arquivados,
                    'clientes_aguard_judicial': clientes_aguard_judicial, 'clientes_aguard_adm': clientes_aguard_adm, 'tarefas_rh': tarefas_rh,
                    'onboardings': onboardings, 'avaliacoes_google': avaliacoes_google, 'cancelados_desistencia': cancelados_desistencia, 'cancelados_docs_direito': cancelados_docs_direito,
                    'advogados': advogados, 'estagiarios': estagiarios, 'auxiliares': auxiliares
                }
                st.success(f"Dados da **{semana_atual}** salvos com sucesso.")
                st.rerun()

    # --- CONSOLIDAÇÃO ---
    totais_mes = {}
    chaves_numericas = [
        'leads_fisico', 'leads_digital', 'qualificados', 'contratos', 'receita_contratada',
        'inss_geral', 'inss_apos_idade', 'inss_apos_tempo', 'inss_invalidez', 'inss_pensao', 'inss_aux_doenca', 'inss_bpc',
        'jf_iniciais', 'jf_apos_idade', 'jf_apos_tempo', 'jf_invalidez', 'jf_bpc', 'sentecas_proc', 'sentecas_improc',
        'faturamento', 'recebido', 'vencido', 'rpv_precatorio', 'pagamento_adm', 'cs_contatos', 'processos_arquivados',
        'clientes_aguard_judicial', 'clientes_aguard_adm', 'tarefas_rh', 'onboardings', 'avaliacoes_google',
        'cancelados_desistencia', 'cancelados_docs_direito', 'advogados', 'estagiarios', 'auxiliares'
    ]

    for chave in chaves_numericas:
        totais_mes[chave] = sum([semana.get(chave, 0) for semana in historico_mes.values()])

    taxa_conversao = (totais_mes['contratos'] / totais_mes['qualificados'] * 100) if totais_mes['qualificados'] > 0 else 0
    inadimplencia_pct = (totais_mes['vencido'] / totais_mes['faturamento'] * 100) if totais_mes['faturamento'] > 0 else 0
    total_aguardando = totais_mes['clientes_aguard_judicial'] + totais_mes['clientes_aguard_adm']
    total_entregue_protocolos = totais_mes['inss_geral'] + totais_mes['jf_iniciais']

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
        st.markdown("#### Comercial (Físico x Digital)")
        f1, f2, f3, f4 = st.columns(4, gap="medium")
        f1.metric("Comercial Físico", totais_mes['leads_fisico'])
        f2.metric("Comercial Digital", totais_mes['leads_digital'])
        f3.metric("Taxa de Conversão", f"{taxa_conversao:.1f}%")
        f4.metric("Receita Contratada", f"R$ {totais_mes['receita_contratada']:,.2f}")

        st.markdown("<div style='margin: 28px 0;'></div>", unsafe_allow_html=True)
        st.markdown("#### Produção Operacional (INSS & JF)")
        op1, op2, op3, op4 = st.columns(4, gap="medium")
        op1.metric("Total Protocolos INSS", totais_mes['inss_geral'])
        op2.metric("Total Iniciais JF", totais_mes['jf_iniciais'])
        op3.metric("Aposentadorias", totais_mes['inss_apos_idade'] + totais_mes['inss_apos_tempo'] + totais_mes['jf_apos_idade'] + totais_mes['jf_apos_tempo'])
        op4.metric("Auxílio Doença", totais_mes['inss_aux_doenca'])

        st.markdown("<div style='margin: 28px 0;'></div>", unsafe_allow_html=True)
        st.markdown("#### Financeiro & Controladoria")
        fi1, fi2, fi3, fi4 = st.columns(4, gap="medium")
        fi1.metric("Inadimplência", f"{inadimplencia_pct:.1f}%", f"R$ {totais_mes['vencido']:,.2f}")
        fi2.metric("RPV / Precatórios", f"R$ {totais_mes['rpv_precatorio']:,.2f}")
        fi3.metric("Pagamento Adm.", f"R$ {totais_mes['pagamento_adm']:,.2f}")
        fi4.metric("Processos Arquivados", totais_mes['processos_arquivados'])

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
        col_p2.metric("Total Entregue (INSS + JF)", total_entregue_protocolos, f"{totais_mes['inss_geral']} INSS / {totais_mes['jf_iniciais']} JF")
        
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
