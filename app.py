import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Controladoria & Gestão | Muller Oliveira", page_icon="⚖️", layout="wide")

# --- DESIGN SYSTEM: DARK MINIMALISTA EXECUTIVO (Muller Oliveira) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #f8fafc; }
    .main { background-color: #0b0f19; }
    
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div, [data-testid="stSidebar"] p {
        color: #f8fafc !important;
    }
    
    h1, h2, h3, h4, p, span, label, div {
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    div[data-testid="stForm"] {
        background-color: #131b2e;
        padding: 28px;
        border-radius: 12px;
        border: 1px solid #1f2937;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stMetric"] {
        background-color: #131b2e;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #1f2937;
        border-left: 3px solid #d4af37;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 13px !important;
    }
    
    .stButton>button {
        background-color: #d4af37 !important;
        color: #0b0f19 !important;
        font-weight: 700;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #e6c547 !important;
        color: #0b0f19 !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #111827;
        border-radius: 6px 6px 0px 0px;
        color: #94a3b8;
        border: 1px solid #1f2937;
        padding: 10px 18px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #131b2e !important;
        color: #d4af37 !important;
        border-bottom: 2px solid #d4af37 !important;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE DADOS NO SESSION STATE ---
if 'usuarios' not in st.session_state:
    # Credenciais iniciais padrão: Administrador e um escritório teste
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

# --- TELA DE LOGIN E RECUPERAÇÃO ---
if st.session_state['usuario_logado'] is None:
    st.markdown("""
        <div style="max-width: 420px; margin: 80px auto; background-color: #111827; padding: 40px; border-radius: 16px; border: 1px solid #1f2937; box-shadow: 0 20px 40px rgba(0,0,0,0.6); text-align: center;">
            <h2 style="color: #ffffff; margin-bottom: 5px; font-weight: 400; letter-spacing: 2px;">MULLER OLIVEIRA</h2>
            <p style="color: #d4af37; font-size: 10px; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 30px;">Controladoria & Gestão Executiva</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_col, col_l2 = st.columns([1, 1.2, 1])
    with col_col:
        aba_login, aba_rec = st.tabs(["🔑 Entrar", "❓ Esqueci a Senha"])
        
        with aba_login:
            with st.form("form_login"):
                usuario_input = st.text_input("Usuário")
                senha_input = st.text_input("Senha", type="password")
                entrar = st.form_submit_button("Acessar Plataforma")
                
                if entrar:
                    if usuario_input in st.session_state['usuarios'] and st.session_state['usuarios'][usuario_input]['senha'] == senha_input:
                        st.session_state['usuario_logado'] = usuario_input
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos.")
                        
        with aba_rec:
            st.markdown("<p style='font-size: 13px; color: #94a3b8; margin-top: 10px;'>Insira seu usuário para solicitar o restablecimento de credenciais ao administrador da consultoria.</p>", unsafe_allow_html=True)
            user_rec = st.text_input("Seu Usuário de Acesso", key="rec_user")
            if st.button("Enviar Solicitação"):
                if user_rec in st.session_state['usuarios']:
                    st.success("Solicitação enviada! O consultor Muller Oliveira entrará em contato com sua nova senha temporária.")
                else:
                    st.warning("Usuário não encontrado na base.")
    st.stop()

# --- USUÁRIO LOGADO ---
user_atual = st.session_state['usuario_logado']
dados_user = st.session_state['usuarios'][user_atual]
is_admin = dados_user['tipo'] == 'admin'

# --- BARRA LATERAL ---
st.sidebar.markdown(f"👤 **Logado como:** {dados_user['nome']}")
if st.sidebar.button("🚪 Sair / Logout"):
    st.session_state['usuario_logado'] = None
    st.rerun()

st.sidebar.markdown("---")

# SE FOR ADMIN, PODE GERENCIAR OS ESCRITÓRIOS
if is_admin:
    st.sidebar.header("⚙️ Painel do Consultor (Admin)")
    
    with st.sidebar.expander("🏢 Cadastrar Novo Escritório"):
        with st.form("cad_escritorio"):
            novo_id = st.text_input("ID de Usuário (Ex: escritorio_b)")
            novo_nome = st.text_input("Nome do Escritório (Ex: Silva & Advogados)")
            nova_senha = st.text_input("Senha de Acesso", type="password")
            salvar_escritorio = st.form_submit_button("Salvar e Criar Acesso")
            
            if salvar_escritorio:
                if novo_id and novo_nome and nova_senha:
                    st.session_state['usuarios'][novo_id] = {"senha": nova_senha, "nome": novo_nome, "tipo": "cliente"}
                    if novo_nome not in st.session_state['base_dados_geral']:
                        st.session_state['base_dados_geral'][novo_nome] = {}
                    st.success(f"Escritório '{novo_nome}' criado com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos.")

    with st.sidebar.expander("🗑️ Excluir Escritório"):
        lista_clientes = [u['nome'] for u in st.session_state['usuarios'].values() if u['tipo'] == 'cliente']
        if lista_clientes:
            escritorio_para_excluir = st.selectbox("Selecione para Excluir", lista_clientes)
            if st.button("Confirmar Exclusão"):
                # Remove do dicionario de usuarios e dados
                chave_del = [k for k, v in st.session_state['usuarios'].items() if v['nome'] == escritorio_para_excluir]
                if chave_del:
                    del st.session_state['usuarios'][chave_del[0]]
                if escritorio_para_excluir in st.session_state['base_dados_geral']:
                    del st.session_state['base_dados_geral'][escritorio_para_excluir]
                st.success(f"Escritório '{escritorio_para_excluir}' excluído!")
                st.rerun()
        else:
            st.info("Nenhum escritório cliente cadastrado.")
            
    st.sidebar.markdown("---")
    # Admin escolhe qual escritório deseja auditar/visualizar
    lista_nomes_clientes = [u['nome'] for u in st.session_state['usuarios'].values() if u['tipo'] == 'cliente']
    if lista_nomes_clientes:
        escritorio_selecionado = st.sidebar.selectbox("Auditar Escritório Cliente", lista_nomes_clientes)
    else:
        escritorio_selecionado = "Nenhum"
else:
    # Se for cliente, ele só vê o escritório dele automaticamente
    escritorio_selecionado = dados_user['nome']
    if escritorio_selecionado not in st.session_state['base_dados_geral']:
        st.session_state['base_dados_geral'][escritorio_selecionado] = {}

st.sidebar.header("📅 Período de Competência")
meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
mes_escolhido = st.sidebar.selectbox("Mês", meses_do_ano, index=7)
ano_escolhido = st.sidebar.number_input("Ano", min_value=2024, max_value=2035, value=2026)
mes_ano_str = f"{mes_escolhido}/{ano_escolhido}"

semana_atual = st.sidebar.selectbox("Selecione a Semana", ["Semana 1", "Semana 2", "Semana 3", "Semana 4"])

# --- CABEÇALHO EXECUTIVO ---
st.markdown(f"""
    <div style="background-color: #111827; padding: 28px 36px; border-radius: 12px; border-bottom: 4px solid #d4af37; margin-bottom: 30px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 10px 25px rgba(0,0,0,0.4);">
        <div>
            <h1 style="margin: 0; font-size: 26px; letter-spacing: 3px; color: #ffffff !important; font-weight: 600;">MULLER OLIVEIRA</h1>
            <p style="margin: 6px 0 0 0; font-size: 11px; letter-spacing: 5px; color: #d4af37 !important; text-transform: uppercase; font-weight: 700;">CONTROLADORIA & GESTÃO EXECUTIVA</p>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 13px; color: #ffffff; background-color: #1f2937; border: 1px solid #374151; padding: 8px 16px; border-radius: 6px; font-weight: 600;">Cliente Ativo: {escritorio_selecionado}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

if escritorio_selecionado == "Nenhum":
    st.warning("⚠️ Nenhum escritório cliente cadastrado. Use o painel administrativo na barra lateral para cadastrar o primeiro cliente.")
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
        "📝 1. Lançamento Semanal", 
        "📊 2. Consolidado Mensal", 
        "⚖️ 3. Previsibilidade (Vendido x Entregue)", 
        "🔍 4. Diagnóstico", 
        "📋 5. Plano de Ação"
    ])

    with tab1:
        st.subheader(f"Lançamento — {escritorio_selecionado} | {mes_ano_str} ({semana_atual})")
        
        if st.button(f"🧹 Limpar Dados de {semana_atual}"):
            st.session_state['base_dados_geral'][escritorio_selecionado][mes_ano_str][semana_atual] = {}
            st.success(f"Dados da {semana_atual} limpos!")
            st.rerun()

        with st.form(f"form_{escritorio_selecionado}_{mes_ano_str}_{semana_atual}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📞 Comercial (Físico & Digital)")
                leads_fisico = st.number_input("Atendimentos Comercial Físico", value=int(dados_semana_salvos.get('leads_fisico', 0)))
                leads_digital = st.number_input("Atendimentos Comercial Digital", value=int(dados_semana_salvos.get('leads_digital', 0)))
                qualificados = st.number_input("Contratos qualificados gerais", value=int(dados_semana_salvos.get('qualificados', 0)))
                contratos = st.number_input("Contratos fechados (Vendido)", value=int(dados_semana_salvos.get('contratos', 0)))
                receita_contratada = st.number_input("Receita contratada (R$)", value=float(dados_semana_salvos.get('receita_contratada', 0.0)))
                
                st.markdown("#### 🏛️ Operacional INSS (Protocolos)")
                inss_geral = st.number_input("Protocolos Adm. INSS Totais", value=int(dados_semana_salvos.get('inss_geral', 0)))
                inss_apos_idade = st.number_input("INSS: Aposentadoria por Idade", value=int(dados_semana_salvos.get('inss_apos_idade', 0)))
                inss_apos_tempo = st.number_input("INSS: Aposentadoria por Tempo/Contribuição", value=int(dados_semana_salvos.get('inss_apos_tempo', 0)))
                inss_invalidez = st.number_input("INSS: Aposentadoria por Invalidez", value=int(dados_semana_salvos.get('inss_invalidez', 0)))
                inss_pensao = st.number_input("INSS: Pensão por Morte", value=int(dados_semana_salvos.get('inss_pensao', 0)))
                inss_aux_doenca = st.number_input("INSS: Auxílio Doença / Incapacidade", value=int(dados_semana_salvos.get('inss_aux_doenca', 0)))
                inss_bpc = st.number_input("INSS: BPC / Loas", value=int(dados_semana_salvos.get('inss_bpc', 0)))

                st.markdown("#### 💰 Financeiro")
                faturamento = st.number_input("Faturamento emitido (R$)", value=float(dados_semana_salvos.get('faturamento', 0.0)))
                recebido = st.number_input("Valor efetivamente recebido (R$)", value=float(dados_semana_salvos.get('recebido', 0.0)))
                vencido = st.number_input("Valor vencido / inadimplente (R$)", value=float(dados_semana_salvos.get('vencido', 0.0)))
                rpv_precatorio = st.number_input("RPV / Precatório recebidos (R$)", value=float(dados_semana_salvos.get('rpv_precatorio', 0.0)))
                pagamento_adm = st.number_input("Pagamento Administrativo (R$)", value=float(dados_semana_salvos.get('pagamento_adm', 0.0)))

            with col2:
                st.markdown("#### ⚖️ Operacional Justiça Federal (JF)")
                jf_iniciais = st.number_input("Protocolos Iniciais JF Totais", value=int(dados_semana_salvos.get('jf_iniciais', 0)))
                jf_apos_idade = st.number_input("JF: Aposentadoria por Idade", value=int(dados_semana_salvos.get('jf_apos_idade', 0)))
                jf_apos_tempo = st.number_input("JF: Aposentadoria por Tempo", value=int(dados_semana_salvos.get('jf_apos_tempo', 0)))
                jf_invalidez = st.number_input("JF: Aposentadoria por Invalidez", value=int(dados_semana_salvos.get('jf_invalidez', 0)))
                jf_bpc = st.number_input("JF: BPC / Loas", value=int(dados_semana_salvos.get('jf_bpc', 0)))
                sentecas_proc = st.number_input("Sentenças procedentes", value=int(dados_semana_salvos.get('sentecas_proc', 0)))
                sentecas_improc = st.number_input("Sentenças improcedentes", value=int(dados_semana_salvos.get('sentecas_improc', 0)))

                st.markdown("#### 🤝 Sucesso do Cliente & Controladoria")
                cs_contatos = st.number_input("Contatos de relacionamento CS", value=int(dados_semana_salvos.get('cs_contatos', 0)))
                processos_arquivados = st.number_input("Processos arquivados", value=int(dados_semana_salvos.get('processos_arquivados', 0)))
                clientes_aguard_judicial = st.number_input("Clientes aguardando envio Judicial", value=int(dados_semana_salvos.get('clientes_aguard_judicial', 0)))
                clientes_aguard_adm = st.number_input("Clientes aguardando envio Administrativo", value=int(dados_semana_salvos.get('clientes_aguard_adm', 0)))

                st.markdown("#### 👥 RH & Qualidade")
                tarefas_rh = st.number_input("Tarefas de RH concluídas", value=int(dados_semana_salvos.get('tarefas_rh', 0)))
                onboardings = st.number_input("Onboardings concluídos", value=int(dados_semana_salvos.get('onboardings', 0)))
                avaliacoes_google = st.number_input("Novas avaliações no Google", value=int(dados_semana_salvos.get('avaliacoes_google', 0)))
                cancelados_desistencia = st.number_input("Cancelados por Desistência", value=int(dados_semana_salvos.get('cancelados_desistencia', 0)))
                cancelados_docs_direito = st.number_input("Cancelados - Docs/Direito", value=int(dados_semana_salvos.get('cancelados_docs_direito', 0)))
                
                st.markdown("#### 🏛️ Equipe Ativa")
                advogados = st.number_input("Advogados", value=int(dados_semana_salvos.get('advogados', 0)))
                estagiarios = st.number_input("Estagiários", value=int(dados_semana_salvos.get('estagiarios', 0)))
                auxiliares = st.number_input("Auxiliares", value=int(dados_semana_salvos.get('auxiliares', 0)))

            submitted = st.form_submit_button(f"💾 Salvar Dados da {semana_atual}")
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
                st.success(f"Dados da **{semana_atual}** salvos para **{escritorio_selecionado}** ({mes_ano_str})!")
                st.rerun()

    # --- Consolidação ---
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
        st.header(f"Consolidado Mensal Controladoria — {escritorio_selecionado} ({mes_ano_str})")
        
        c1, c2, c3, c4 = st.columns(4)
        status_score = "Aguardando Dados" if score_geral == 0 else "Consolidado"
        c1.metric("Score de Gestão", f"{score_geral:.0f} / 100", status_score)
        c2.metric("Total Vendido (Contratos)", totais_mes['contratos'])
        c3.metric("Faturamento Consolidado", f"R$ {totais_mes['faturamento']:,.2f}")
        c4.metric("Recebido Efetivo", f"R$ {totais_mes['recebido']:,.2f}")

        st.markdown("---")
        st.subheader("📞 Comercial (Físico x Digital)")
        f1, f2, f3, f4 = st.columns(4)
        f1.metric("Comercial Físico", totais_mes['leads_fisico'])
        f2.metric("Comercial Digital", totais_mes['leads_digital'])
        f3.metric("Taxa de Conversão", f"{taxa_conversao:.1f}%")
        f4.metric("Receita Contratada", f"R$ {totais_mes['receita_contratada']:,.2f}")

        st.markdown("---")
        st.subheader("🏛️ Produção Operacional (INSS & JF por Benefício)")
        op1, op2, op3, op4 = st.columns(4)
        op1.metric("Total Protocolos INSS", totais_mes['inss_geral'])
        op2.metric("Total Iniciais Justiça Federal", totais_mes['jf_iniciais'])
        op3.metric("Aposentadorias (INSS+JF)", totais_mes['inss_apos_idade'] + totais_mes['inss_apos_tempo'] + totais_mes['jf_apos_idade'] + totais_mes['jf_apos_tempo'])
        op4.metric("Auxílio Doença / Incapacidade", totais_mes['inss_aux_doenca'])

        st.markdown("---")
        st.subheader("💰 Financeiro & Controladoria")
        fi1, fi2, fi3, fi4 = st.columns(4)
        fi1.metric("Inadimplência", f"{inadimplencia_pct:.1f}%", f"R$ {totais_mes['vencido']:,.2f}")
        fi2.metric("RPV / Precatórios", f"R$ {totais_mes['rpv_precatorio']:,.2f}")
        fi3.metric("Pagamento Administrativo", f"R$ {totais_mes['pagamento_adm']:,.2f}")
        fi4.metric("Processos Arquivados", totais_mes['processos_arquivados'])

        st.markdown("---")
        st.subheader("📊 Histórico Detalhado por Semana")
        df_semanas = pd.DataFrame(historico_mes).T
        st.dataframe(df_semanas, use_container_width=True)

    with tab3:
        st.header(f"Previsibilidade: Vendido vs. Entregue — {escritorio_selecionado}")
        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.metric("Total Vendido no Mês", totais_mes['contratos'])
        col_p2.metric("Total Entregue (INSS + JF)", total_entregue_protocolos, f"{totais_mes['inss_geral']} INSS / {totais_mes['jf_iniciais']} JF")
        
        indice_vazao = (total_entregue_protocolos / totais_mes['contratos'] * 100) if totais_mes['contratos'] > 0 else 0
        col_p3.metric("Índice de Vazão Mensal", f"{indice_vazao:.1f}%", "Meta: 100%")

    with tab4:
        st.header(f"Diagnóstico de Estoques — {escritorio_selecionado}")
        if score_geral == 0:
            st.info("Preencha as semanas para gerar o diagnóstico.")
        else:
            st.error("🚨 **PONTOS DE ATENÇÃO OPERACIONAL**")
            st.write(f"Há **{total_aguardando} clientes** parados na esteira de envio e demanda reprimida nos protocolos.")

    with tab5:
        st.header("📋 Plano de Ação Estratégico")
        if score_geral == 0:
            st.info("Preencha as semanas para gerar o plano de ação.")
        else:
            st.markdown(f"* **Foco Comercial:** Acelerar conversão digital e física frente aos {totais_mes['qualificados']} qualificados.")
            st.markdown(f"* **Foco Retenção:** Tratar cancelamentos por desistência ({totais_mes['cancelados_desistencia']}) e docs/direito ({totais_mes['cancelados_docs_direito']}).")
