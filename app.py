import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Controladoria & Gestão Executiva | Muller Oliveira", 
    page_icon="⚖️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DESIGN SYSTEM: SOFTWARE EXECUTIVO SaaS (UI/UX PREMIUM) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-main: #080F1A;
        --bg-sidebar: #0D1726;
        --bg-card: #121D31;
        --bg-card-secondary: #16233A;
        --border: #263550;

        --gold: #D6B238;
        --gold-hover: #E4C456;

        --text-primary: #F4F6FA;
        --text-secondary: #AAB4C4;

        --input-bg: #F4F5F7;
        --input-text: #20283A;

        --danger: #C86666;
        --danger-hover: #D97777;

        --radius-sm: 8px;
        --radius-md: 10px;
        --radius-lg: 16px;
        --radius-xl: 18px;
    }

    /* Aplicação Geral */
    .stApp {
        background-color: var(--bg-main);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-sidebar);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] div, 
    section[data-testid="stSidebar"] p {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
    }

    /* Tipografia de Títulos Globais */
    h1, h2, h3, h4 {
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }

    /* Inputs e Selects */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: var(--input-bg) !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid transparent !important;
    }
    div[data-baseweb="input"] input, div[data-baseweb="select"] span {
        color: var(--input-text) !important;
    }
    .stNumberInput input {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid transparent !important;
    }
    .stTextInput input {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border-radius: var(--radius-md) !important;
    }

    /* Formulários Executivos */
    div[data-testid="stForm"] {
        background-color: var(--bg-card);
        padding: 28px;
        border-radius: var(--radius-lg);
        border: 1px solid var(--border);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    /* Cards de Métricas */
    [data-testid="stMetric"] {
        background-color: var(--bg-card);
        padding: 20px;
        border-radius: var(--radius-md);
        border: 1px solid var(--border);
        border-left: 3px solid var(--gold);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 13px !important;
        font-weight: 500;
    }

    /* Botões Primários Padronizados (Dourados) */
    .stButton > button[kind="primary"], div.stButton > button:first-child {
        background-color: var(--gold) !important;
        color: #101827 !important;
        border: 1px solid var(--gold) !important;
        border-radius: var(--radius-md) !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover, div.stButton > button:first-child:hover {
        background-color: var(--gold-hover) !important;
        border-color: var(--gold-hover) !important;
        color: #080F1A !important;
        box-shadow: 0 0 15px rgba(214, 178, 56, 0.3);
    }

    /* Abas de Navegação Superior */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: transparent;
        border-bottom: 1px solid var(--border);
        padding-bottom: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: var(--bg-sidebar);
        border-radius: var(--radius-sm) var(--radius-sm) 0px 0px;
        color: var(--text-secondary);
        border: 1px solid var(--border);
        border-bottom: none;
        padding: 10px 18px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-bottom: 3px solid var(--gold) !important;
        font-weight: 600 !important;
    }

    /* Estilos de Marca Customizados */
    .brand-serif {
        font-family: 'Cormorant Garamond', serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE DADOS NO SESSION STATE ---
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = {
        "admin": {"senha": "muller2026", "nome": "Muller Oliveira (Admin)", "tipo": "admin"},
        "escritorio_a": {"senha": "123", "nome": "T.A. Advocacia", "tipo": "cliente"}
    }

if 'base_dados_geral' not in st.session_state:
    st.session_state['base_dados_geral'] = {
        "T.A. Advocacia": {}
    }

if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = None

# --- TELA DE AUTENTICAÇÃO (LOGIN / RECUPERAÇÃO) ---
if st.session_state['usuario_logado'] is None:
    st.markdown("""
        <div style="max-width: 420px; margin: 90px auto; background-color: #0D1726; padding: 42px; border-radius: 18px; border: 1px solid #263550; box-shadow: 0 25px 50px rgba(0,0,0,0.7); text-align: center;">
            <h2 class="brand-serif" style="color: #F4F6FA; margin-bottom: 4px; font-size: 32px; font-weight: 600; letter-spacing: 2px;">Muller Oliveira</h2>
            <p style="color: #D6B238; font-size: 10px; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 32px; font-weight: 600;">Controladoria & Gestão Executiva</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_col, col_l2 = st.columns([1, 1.2, 1])
    with col_col:
        aba_login, aba_rec = st.tabs(["Acesso Executivo", "Recuperar Senha"])
        
        with aba_login:
            with st.form("form_login"):
                st.markdown("<p style='font-size: 13px; color: #AAB4C4; margin-bottom: 12px;'>Entre com suas credenciais corporativas.</p>", unsafe_allow_html=True)
                usuario_input = st.text_input("Usuário de acesso")
                senha_input = st.text_input("Senha", type="password")
                entrar = st.form_submit_button("Acessar plataforma", icon=":material/login:")
                
                if entrar:
                    if usuario_input in st.session_state['usuarios'] and st.session_state['usuarios'][usuario_input]['senha'] == senha_input:
                        st.session_state['usuario_logado'] = usuario_input
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas. Verifique seu usuário e senha.")
                        
        with aba_rec:
            st.markdown("<p style='font-size: 13px; color: #AAB4C4; margin-top: 10px;'>Informe seu usuário para solicitar o reestabelecimento de credenciais.</p>", unsafe_allow_html=True)
            user_rec = st.text_input("Usuário cadastrado", key="rec_user")
            if st.button("Enviar solicitação", icon=":material/send:", type="secondary"):
                if user_rec in st.session_state['usuarios']:
                    st.success("Solicitação enviada. O administrador entrará em contato.")
                else:
                    st.warning("Usuário não localizado na base.")
    st.stop()

# --- SESSÃO ATIVA & SIDEBAR EXECUTIVA ---
user_atual = st.session_state['usuario_logado']
dados_user = st.session_state['usuarios'][user_atual]
is_admin = dados_user['tipo'] == 'admin'

st.sidebar.markdown(f"**Sessão Ativa**\n\n`{dados_user['nome']}`")
if st.sidebar.button("Encerrar sessão", icon=":material/logout:", type="secondary"):
    st.session_state['usuario_logado'] = None
    st.rerun()

st.sidebar.markdown("---")

if is_admin:
    st.sidebar.markdown("### Painel do Consultor")
    
    with st.sidebar.expander("Gerenciar escritórios", expanded=False):
        with st.form("cad_escritorio"):
            st.markdown("**Cadastrar novo escritório**")
            novo_id = st.text_input("Usuário de acesso", placeholder="escritorio_b")
            novo_nome = st.text_input("Nome do escritório", placeholder="Nayara Lira Advocacia")
            nova_senha = st.text_input("Senha", type="password")
            salvar_escritorio = st.form_submit_button("Criar acesso", icon=":material/add_business:")
            
            if salvar_escritorio:
                if novo_id and novo_nome and nova_senha:
                    st.session_state['usuarios'][novo_id] = {"senha": nova_senha, "nome": novo_nome, "tipo": "cliente"}
                    if novo_nome not in st.session_state['base_dados_geral']:
                        st.session_state['base_dados_geral'][novo_nome] = {}
                    st.success(f"Escritório '{novo_nome}' criado com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos obrigatórios.")

        st.markdown("---")
        st.markdown("**Remover escritório**")
        lista_clientes = [u['nome'] for u in st.session_state['usuarios'].values() if u['tipo'] == 'cliente']
        if lista_clientes:
            escritorio_para_excluir = st.selectbox("Selecione o escritório", lista_clientes, key="del_esc")
            if st.button("Excluir escritório", icon=":material/delete:", type="secondary"):
                chave_del = [k for k, v in st.session_state['usuarios'].items() if v['nome'] == escritorio_para_excluir]
                if chave_del:
                    del st.session_state['usuarios'][chave_del[0]]
                if escritorio_para_excluir in st.session_state['base_dados_geral']:
                    del st.session_state['base_dados_geral'][escritorio_para_excluir]
                st.success(f"Escritório '{escritorio_para_excluir}' removido.")
                st.rerun()
        else:
            st.info("Nenhum cliente cadastrado.")

    st.sidebar.markdown("---")
    lista_nomes_clientes = [u['nome'] for u in st.session_state['usuarios'].values() if u['tipo'] == 'cliente']
    if lista_nomes_clientes:
        escritorio_selecionado = st.sidebar.selectbox("Escritório ativo", lista_nomes_clientes)
    else:
        escritorio_selecionado = "Nenhum"
else:
    escritorio_selecionado = dados_user['nome']
    if escritorio_selecionado not in st.session_state['base_dados_geral']:
        st.session_state['base_dados_geral'][escritorio_selecionado] = {}

st.sidebar.markdown("### Período de Competência")
meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
mes_escolhido = st.sidebar.selectbox("Mês", meses_do_ano, index=7)
ano_escolhido = st.sidebar.number_input("Ano", min_value=2024, max_value=2035, value=2026)
mes_ano_str = f"{mes_escolhido}/{ano_escolhido}"

semana_atual = st.sidebar.selectbox("Semana de Referência", ["Semana 1", "Semana 2", "Semana 3", "Semana 4"])

# --- CABEÇALHO PRINCIPAL EXECUTIVO ---
st.markdown(f"""
    <div style="background-color: #0D1726; padding: 28px 36px; border-radius: 16px; border: 1px solid #263550; border-bottom: 4px solid #D6B238; margin-bottom: 30px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
        <div>
            <h1 class="brand-serif" style="margin: 0; font-size: 30px; letter-spacing: 2px; color: #F4F6FA !important; font-weight: 600;">Muller Oliveira</h1>
            <p style="margin: 6px 0 0 0; font-size: 11px; letter-spacing: 4px; color: #D6B238 !important; text-transform: uppercase; font-weight: 600;">Controladoria & Gestão Executiva</p>
        </div>
        <div style="text-align: right; background-color: #121D31; border: 1px solid #263550; padding: 10px 18px; border-radius: 10px;">
            <div style="font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase; color: #AAB4C4; margin-bottom: 2px;">Cliente Ativo</div>
            <div style="font-size: 15px; font-weight: 600; color: #F4F6FA;">{escritorio_selecionado}</div>
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
            st.markdown(f"### Lançamento Semanal\n**{escritorio_selecionado}** · {mes_escolhido} de {ano_escolhido} · {semana_atual}")
        with col_t2:
            if st.button("Limpar dados da semana", icon=":material/cleaning_services:", type="secondary"):
                st.session_state['base_dados_geral'][escritorio_selecionado][mes_ano_str][semana_atual] = {}
                st.success(f"Dados da {semana_atual} limpos.")
                st.rerun()

        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

        with st.form(f"form_{escritorio_selecionado}_{mes_ano_str}_{semana_atual}"):
            col1, col2 = st.columns(2)
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

            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Salvar alterações", icon=":material/save:", type="primary")
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
        st.markdown(f"### Consolidado Mensal\n**{escritorio_selecionado}** · {mes_escolhido} de {ano_escolhido}")
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        status_score = "Aguardando dados" if score_geral == 0 else "Consolidado"
        c1.metric("Score de Gestão", f"{score_geral:.0f} / 100", status_score)
        c2.metric("Total Vendido", totais_mes['contratos'])
        c3.metric("Faturamento", f"R$ {totais_mes['faturamento']:,.2f}")
        c4.metric("Recebido Efetivo", f"R$ {totais_mes['recebido']:,.2f}")

        st.markdown("---")
        st.markdown("#### Comercial (Físico x Digital)")
        f1, f2, f3, f4 = st.columns(4)
        f1.metric("Comercial Físico", totais_mes['leads_fisico'])
        f2.metric("Comercial Digital", totais_mes['leads_digital'])
        f3.metric("Taxa de Conversão", f"{taxa_conversao:.1f}%")
        f4.metric("Receita Contratada", f"R$ {totais_mes['receita_contratada']:,.2f}")

        st.markdown("---")
        st.markdown("#### Produção Operacional (INSS & JF)")
        op1, op2, op3, op4 = st.columns(4)
        op1.metric("Total Protocolos INSS", totais_mes['inss_geral'])
        op2.metric("Total Iniciais JF", totais_mes['jf_iniciais'])
        op3.metric("Aposentadorias (INSS+JF)", totais_mes['inss_apos_idade'] + totais_mes['inss_apos_tempo'] + totais_mes['jf_apos_idade'] + totais_mes['jf_apos_tempo'])
        op4.metric("Auxílio Doença", totais_mes['inss_aux_doenca'])

        st.markdown("---")
        st.markdown("#### Financeiro & Controladoria")
        fi1, fi2, fi3, fi4 = st.columns(4)
        fi1.metric("Inadimplência", f"{inadimplencia_pct:.1f}%", f"R$ {totais_mes['vencido']:,.2f}")
        fi2.metric("RPV / Precatórios", f"R$ {totais_mes['rpv_precatorio']:,.2f}")
        fi3.metric("Pagamento Administrativo", f"R$ {totais_mes['pagamento_adm']:,.2f}")
        fi4.metric("Processos Arquivados", totais_mes['processos_arquivados'])

        st.markdown("---")
        st.markdown("#### Histórico Detalhado por Semana")
        df_semanas = pd.DataFrame(historico_mes).T
        st.dataframe(df_semanas, use_container_width=True)

    with tab3:
        st.markdown(f"### Previsibilidade (Vendido x Entregue)\n**{escritorio_selecionado}**")
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        
        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.metric("Total Vendido no Mês", totais_mes['contratos'])
        col_p2.metric("Total Entregue (INSS + JF)", total_entregue_protocolos, f"{totais_mes['inss_geral']} INSS / {totais_mes['jf_iniciais']} JF")
        
        indice_vazao = (total_entregue_protocolos / totais_mes['contratos'] * 100) if totais_mes['contratos'] > 0 else 0
        col_p3.metric("Índice de Vazão Mensal", f"{indice_vazao:.1f}%", "Meta: 100%")

    with tab4:
        st.markdown(f"### Diagnóstico de Estoques\n**{escritorio_selecionado}**")
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        
        if score_geral == 0:
            st.info("Preencha os dados das semanas para gerar o diagnóstico executivo.")
        else:
            st.error("Pontos de Atenção Operacional")
            st.write(f"Há **{total_aguardando} clientes** parados na esteira aguardando encaminhamento para o contencioso judicial ou administrativo.")

    with tab5:
        st.markdown(f"### Plano de Ação Estratégico\n**{escritorio_selecionado}**")
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        
        if score_geral == 0:
            st.info("Preencha os dados das semanas para gerar as diretrizes do plano de ação.")
        else:
            st.markdown(f"* **Foco Comercial:** Acelerar conversão digital e física frente aos {totais_mes['qualificados']} qualificados registrados no período.")
            st.markdown(f"* **Foco Retenção:** Tratar cancelamentos por desistência ({totais_mes['cancelados_desistencia']}) e docs/direito ({totais_mes['cancelados_docs_direito']}).")
