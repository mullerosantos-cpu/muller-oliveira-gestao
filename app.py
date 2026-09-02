import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Controladoria & Gestão Executiva | Muller Oliveira", 
    page_icon="⚖️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DESIGN SYSTEM EXECUTIVO: BLINDAGEM DE CSS & TOKENS OFICIAIS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg: #080E18;
        --sidebar: #0D1726;
        --surface: #111C2E;
        --surface-2: #152238;
        --border: #26354D;
        --text: #F2F4F7;
        --text-2: #98A4B5;
        --text-3: #6F7B8D;
        --gold: #D8B43C;
        --gold-hover: #E3C355;
        --danger: #C96C6C;
        --success: #3F9C6B;
        --radius-input: 9px;
        --radius-button: 9px;
        --radius-card: 14px;
    }

    /* Fundo Geral */
    .stApp {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Sidebar Limpa e Alinhada */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar) !important;
        border-right: 1px solid var(--border) !important;
        padding-top: 1rem !important;
    }
    section[data-testid="stSidebar"] * {
        font-family: 'Inter', sans-serif !important;
        color: var(--text) !important;
    }

    /* Tipografia de Títulos */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text) !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em;
    }
    .brand-serif {
        font-family: 'Cormorant Garamond', serif !important;
    }

    /* Inputs Padrão */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #F3F4F6 !important;
        border-radius: var(--radius-input) !important;
        border: 1px solid transparent !important;
        min-height: 42px !important;
    }
    div[data-baseweb="input"] input, div[data-baseweb="select"] span {
        color: #202738 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
    }
    .stNumberInput input, .stTextInput input {
        background-color: #F3F4F6 !important;
        color: #202738 !important;
        border-radius: var(--radius-input) !important;
        font-size: 14px !important;
    }

    /* Formulários e Superfícies */
    div[data-testid="stForm"] {
        background-color: var(--surface) !important;
        padding: 24px !important;
        border-radius: var(--radius-card) !important;
        border: 1px solid var(--border) !important;
    }

    /* Métricas Compactas */
    [data-testid="stMetric"] {
        background-color: var(--surface) !important;
        padding: 16px 20px !important;
        border-radius: var(--radius-card) !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-2) !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }

    /* Botões Primários Dourados */
    .stButton > button[kind="primary"], div.stButton > button:first-child {
        background-color: var(--gold) !important;
        color: #080E18 !important;
        border: 1px solid var(--gold) !important;
        border-radius: var(--radius-button) !important;
        font-weight: 600 !important;
        height: 42px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover, div.stButton > button:first-child:hover {
        background-color: var(--gold-hover) !important;
        border-color: var(--gold-hover) !important;
        color: #080E18 !important;
        box-shadow: 0 0 12px rgba(216, 180, 60, 0.25);
    }

    /* Botões Secundários */
    .stButton > button[kind="secondary"] {
        background-color: var(--surface-2) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-button) !important;
        height: 40px !important;
        font-weight: 500 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #1A2B45 !important;
        border-color: #3A4C68 !important;
        color: var(--text) !important;
    }

    /* Navegação por Abas Limpa */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent !important;
        border-bottom: 1px solid var(--border) !important;
        margin-bottom: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: var(--text-3) !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        padding: 10px 16px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #D4D9E1 !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--text) !important;
        border-bottom: 2px solid var(--gold) !important;
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

# --- TELA DE AUTENTICAÇÃO EXECUTIVA ---
if st.session_state['usuario_logado'] is None:
    st.markdown("""
        <div style="max-width: 400px; margin: 100px auto; background-color: #111C2E; padding: 36px; border-radius: 16px; border: 1px solid #26354D; box-shadow: 0 20px 40px rgba(0,0,0,0.6); text-align: center;">
            <h2 class="brand-serif" style="color: #F2F4F7; margin-bottom: 2px; font-size: 32px; font-weight: 600;">Muller Oliveira</h2>
            <p style="color: #D8B43C; font-size: 10px; letter-spacing: 0.25em; text-transform: uppercase; margin-bottom: 28px; font-weight: 600;">Controladoria & Gestão Executiva</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_col, col_l2 = st.columns([1, 1.2, 1])
    with col_col:
        aba_login, aba_rec = st.tabs(["Acesso", "Recuperar"])
        
        with aba_login:
            with st.form("form_login"):
                st.markdown("<p style='font-size: 13px; color: #98A4B5; margin-bottom: 12px;'>Informe suas credenciais corporativas.</p>", unsafe_allow_html=True)
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
            st.markdown("<p style='font-size: 13px; color: #98A4B5; margin-top: 10px;'>Solicite o reestabelecimento ao administrador.</p>", unsafe_allow_html=True)
            user_rec = st.text_input("Usuário cadastrado", key="rec_user")
            if st.button("Enviar solicitação", type="secondary", use_container_width=True):
                if user_rec in st.session_state['usuarios']:
                    st.success("Solicitação enviada com sucesso.")
                else:
                    st.warning("Usuário não localizado.")
    st.stop()

# --- SESSÃO ATIVA & SIDEBAR REESTRUTURADA ---
user_atual = st.session_state['usuario_logado']
dados_user = st.session_state['usuarios'][user_atual]
is_admin = dados_user['tipo'] == 'admin'

st.sidebar.markdown("<div style='font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #6F7B8D; margin-bottom: 4px;'>Sessão ativa</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"""
    <div style="background-color: #152238; border: 1px solid #26354D; border-radius: 8px; padding: 10px 12px; margin-bottom: 12px;">
        <div style="font-size: 13px; font-weight: 500; color: #F2F4F7;">{dados_user['nome']}</div>
        <div style="font-size: 11px; color: #98A4B5; margin-top: 2px;">{'Administrador' : 'Cliente Corporativo'}</div>
    </div>
""", unsafe_allow_html=True)

if st.sidebar.button("Encerrar sessão", type="secondary", use_container_width=True):
    st.session_state['usuario_logado'] = None
    st.rerun()

st.sidebar.markdown("---")

if is_admin:
    st.sidebar.markdown("<div style='font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #6F7B8D; margin-bottom: 8px;'>Painel do Consultor</div>", unsafe_allow_html=True)
    
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
        st.sidebar.markdown("<div style='font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #6F7B8D; margin-bottom: 4px;'>Escritório Ativo</div>", unsafe_allow_html=True)
        escritorio_selecionado = st.sidebar.selectbox("Selecionar escritório ativo", lista_nomes_clientes, label_visibility="collapsed")
    else:
        escritorio_selecionado = "Nenhum"
else:
    escritorio_selecionado = dados_user['nome']
    if escritorio_selecionado not in st.session_state['base_dados_geral']:
        st.session_state['base_dados_geral'][escritorio_selecionado] = {}

st.sidebar.markdown("<div style='font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #6F7B8D; margin-bottom: 8px;'>Período de Competência</div>", unsafe_allow_html=True)
meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
mes_escolhido = st.sidebar.selectbox("Mês", meses_do_ano, index=7)
ano_escolhido = st.sidebar.number_input("Ano", min_value=2024, max_value=2035, value=2026)
mes_ano_str = f"{mes_escolhido}/{ano_escolhido}"

semana_atual = st.sidebar.selectbox("Semana de Referência", ["Semana 1", "Semana 2", "Semana 3", "Semana 4"])

# --- CABEÇALHO EXECUTIVO MINIMALISTA ---
st.markdown(f"""
    <div style="background-color: #0D1726; padding: 26px 36px; border-radius: 14px; border: 1px solid #26354D; border-bottom: 3px solid #D8B43C; margin-bottom: 32px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 8px 24px rgba(0,0,0,0.35);">
        <div>
            <h1 class="brand-serif" style="margin: 0; font-size: 36px; font-weight: 600; line-height: 1; color: #F2F4F7 !important;">Muller Oliveira</h1>
            <p style="margin: 12px 0 0 0; font-size: 11px; letter-spacing: 0.28em; color: #A9B1BF !important; text-transform: uppercase; font-weight: 600;">Controladoria & Gestão Executiva</p>
        </div>
        <div style="background-color: #111C2E; border: 1px solid #26354D; padding: 12px 16px; border-radius: 10px;">
            <div style="font-size: 9px; letter-spacing: 0.14em; text-transform: uppercase; color: #8E99A9; margin-bottom: 2px;">Cliente Ativo</div>
            <div style="font-size: 14px; font-weight: 600; color: #F2F4F7;">{escritorio_selecionado}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

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
                    <h2 style="font-size: 32px; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 8px 0;">Lançamento semanal</h2>
                    <div style="font-size: 15px; font-weight: 500; color: #98A4B5;"><span style="color: #F2F4F7;">{escritorio_selecionado}</span> · {mes_escolhido} de {ano_escolhido} · {semana_atual}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_t2:
            st.markdown("<div style='padding-top: 4px;'></div>", unsafe_allow_html=True)
            if st.button("Limpar dados da semana", type="secondary"):
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
                <h2 style="font-size: 32px; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 8px 0;">Consolidado mensal</h2>
                <div style="font-size: 15px; font-weight: 500; color: #98A4B5;"><span style="color: #F2F4F7;">{escritorio_selecionado}</span> · {mes_escolhido} de {ano_escolhido}</div>
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
                <h2 style="font-size: 32px; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 8px 0;">Previsibilidade</h2>
                <div style="font-size: 15px; font-weight: 500; color: #98A4B5;">Vendido x Entregue · <span style="color: #F2F4F7;">{escritorio_selecionado}</span></div>
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
                <h2 style="font-size: 32px; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 8px 0;">Diagnóstico</h2>
                <div style="font-size: 15px; font-weight: 500; color: #98A4B5;">Análise de estoques · <span style="color: #F2F4F7;">{escritorio_selecionado}</span></div>
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
                <h2 style="font-size: 32px; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 8px 0;">Plano de ação</h2>
                <div style="font-size: 15px; font-weight: 500; color: #98A4B5;">Diretrizes estratégicas · <span style="color: #F2F4F7;">{escritorio_selecionado}</span></div>
            </div>
        """, unsafe_allow_html=True)
        
        if score_geral == 0:
            st.info("Preencha os dados das semanas para gerar as diretrizes do plano de ação.")
        else:
            st.markdown(f"* **Foco Comercial:** Acelerar conversão digital e física frente aos {totais_mes['qualificados']} qualificados registrados no período.")
            st.markdown(f"* **Foco Retenção:** Tratar cancelamentos por desistência ({totais_mes['cancelados_desistencia']}) e docs/direito ({totais_mes['cancelados_docs_direito']}).")
