import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Diagnóstico e Gestão | Muller Oliveira", page_icon="⚖️", layout="wide")

# --- DESIGN SYSTEM EXECUTIVO ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #0f172a; }
    .main { background-color: #f8fafc; }
    
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #cbd5e1;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div, [data-testid="stSidebar"] p {
        color: #ffffff !important;
    }
    
    h1, h2, h3, h4, p, span, label, div {
        color: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    div[data-testid="stForm"] {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #d4af37;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    }
    [data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 700;
    }
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 13px !important;
    }
    
    .stButton>button {
        background-color: #d4af37 !important;
        color: #0f172a !important;
        font-weight: 700;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #c29f2e !important;
        color: #ffffff !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e2e8f0;
        border-radius: 6px 6px 0px 0px;
        color: #475569;
        border: 1px solid #cbd5e1;
        padding: 10px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-bottom: 2px solid #d4af37 !important;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO EXECUTIVO ---
st.markdown("""
    <div style="background-color: #1e293b; padding: 28px 36px; border-radius: 12px; border-bottom: 4px solid #d4af37; margin-bottom: 30px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
        <div>
            <h1 style="margin: 0; font-size: 26px; letter-spacing: 3px; color: #ffffff !important; font-weight: 600;">MULLER OLIVEIRA</h1>
            <p style="margin: 6px 0 0 0; font-size: 11px; letter-spacing: 5px; color: #d4af37 !important; text-transform: uppercase; font-weight: 700;">CONSULTORIA & GESTÃO</p>
        </div>
        <div>
            <span style="font-size: 12px; color: #ffffff; background-color: #334155; border: 1px solid #475569; padding: 8px 16px; border-radius: 6px; font-weight: 600; letter-spacing: 1px;">PLATAFORMA EXECUTIVA</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Gestão de Escritórios ---
if 'lista_escritorios' not in st.session_state:
    st.session_state['lista_escritorios'] = []

if 'base_dados_geral' not in st.session_state:
    st.session_state['base_dados_geral'] = {}

st.sidebar.header("🏢 Gestão de Escritórios")

novo_escritorio = st.sidebar.text_input("Cadastrar Novo Escritório")
if st.sidebar.button("➕ Adicionar Escritório"):
    if novo_escritorio and novo_escritorio not in st.session_state['lista_escritorios']:
        st.session_state['lista_escritorios'].append(novo_escritorio)
        st.session_state['base_dados_geral'][novo_escritorio] = {}
        st.sidebar.success(f"Escritório '{novo_escritorio}' cadastrado!")
        st.rerun()

st.sidebar.markdown("---")

if len(st.session_state['lista_escritorios']) > 0:
    escritorio_selecionado = st.sidebar.selectbox("Selecionar Escritório Ativo", st.session_state['lista_escritorios'])

    if st.sidebar.button("🗑️ Excluir Escritório Selecionado"):
        st.session_state['lista_escritorios'].remove(escritorio_selecionado)
        del st.session_state['base_dados_geral'][escritorio_selecionado]
        st.sidebar.success("Escritório excluído!")
        st.rerun()
else:
    escritorio_selecionado = None
    st.sidebar.info("Nenhum escritório cadastrado. Cadastre acima para começar.")

st.sidebar.markdown("---")
st.sidebar.header("📅 Período de Competência")
meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
mes_escolhido = st.sidebar.selectbox("Mês", meses_do_ano, index=7)
ano_escolhido = st.sidebar.number_input("Ano", min_value=2024, max_value=2035, value=2026)
mes_ano_str = f"{mes_escolhido}/{ano_escolhido}"

semana_atual = st.sidebar.selectbox("Selecione a Semana", ["Semana 1", "Semana 2", "Semana 3", "Semana 4"])

if not escritorio_selecionado:
    st.warning("⚠️ Por favor, cadastre e selecione um escritório na barra lateral para iniciar os lançamentos.")
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
                st.markdown("#### 🎯 Comercial & Relacionamento")
                leads = st.number_input("Leads recebidos", value=int(dados_semana_salvos.get('leads', 0)))
                qualificados = st.number_input("Leads qualificados", value=int(dados_semana_salvos.get('qualificados', 0)))
                contratos = st.number_input("Contratos fechados (Vendido)", value=int(dados_semana_salvos.get('contratos', 0)))
                contratos_cancelados = st.number_input("Contratos cancelados (Geral)", value=int(dados_semana_salvos.get('contratos_cancelados', 0)))
                receita_contratada = st.number_input("Receita contratada (R$)", value=float(dados_semana_salvos.get('receita_contratada', 0.0)))
                
                st.markdown("#### 📥 Esteira de Clientes (Aguardando)")
                clientes_aguard_judicial = st.number_input("Clientes aguardando envio ao Judicial", value=int(dados_semana_salvos.get('clientes_aguard_judicial', 0)))
                clientes_aguard_adm = st.number_input("Clientes aguardando envio ao Administrativo", value=int(dados_semana_salvos.get('clientes_aguard_adm', 0)))

                st.markdown("#### 💰 Financeiro")
                faturamento = st.number_input("Faturamento emitido (R$)", value=float(dados_semana_salvos.get('faturamento', 0.0)))
                recebido = st.number_input("Valor efetivamente recebido (R$)", value=float(dados_semana_salvos.get('recebido', 0.0)))
                vencido = st.number_input("Valor vencido / inadimplente (R$)", value=float(dados_semana_salvos.get('vencido', 0.0)))
                rpv_precatorio = st.number_input("RPV / Precatório (R$)", value=float(dados_semana_salvos.get('rpv_precatorio', 0.0)))
                pagamento_adm = st.number_input("Pagamento Administrativo (R$)", value=float(dados_semana_salvos.get('pagamento_adm', 0.0)))
                
                st.markdown("#### 👥 Equipe")
                advogados = st.number_input("Advogados", value=int(dados_semana_salvos.get('advogados', 0)))
                estagiarios = st.number_input("Estagiários", value=int(dados_semana_salvos.get('estagiarios', 0)))
                auxiliares = st.number_input("Auxiliares", value=int(dados_semana_salvos.get('auxiliares', 0)))
                assistentes = st.number_input("Assistentes", value=int(dados_semana_salvos.get('assistentes', 0)))

            with col2:
                st.markdown("#### ⚖️ Operação Judicial")
                processos_ativos_jud = st.number_input("Processos ativos atuais (Estoque)", value=int(dados_semana_salvos.get('processos_ativos_jud', 0)))
                aguard_revisao_jud = st.number_input("Estoque: Aguardando revisão", value=int(dados_semana_salvos.get('aguard_revisao_jud', 0)))
                aguard_protocolo_jud = st.number_input("Estoque: Aguardando protocolos", value=int(dados_semana_salvos.get('aguard_protocolo_jud', 0)))
                protocolados_mes = st.number_input("Protocolos de inicial realizados", value=int(dados_semana_salvos.get('protocolados_mes', 0)))
                protocolados_prazo_fatal = st.number_input("Protocolos realizados NO PRAZO FATAL", value=int(dados_semana_salvos.get('protocolados_prazo_fatal', 0)))
                emendas_inicial = st.number_input("Emendas à Inicial recebidas", value=int(dados_semana_salvos.get('emendas_inicial', 0)))
                
                sentecas_proc = st.number_input("Sentenças procedentes", value=int(dados_semana_salvos.get('sentecas_proc', 0)))
                sentecas_improc = st.number_input("Sentenças improcedentes", value=int(dados_semana_salvos.get('sentecas_improc', 0)))
                extintos_sem_merito = st.number_input("Extintos sem resolução do mérito", value=int(dados_semana_salvos.get('extintos_sem_merito', 0)))
                desistencias_jud = st.number_input("Desistências no processo judicial", value=int(dados_semana_salvos.get('desistencias_jud', 0)))
                
                recursos_interpostos = st.number_input("Recursos interpostos", value=int(dados_semana_salvos.get('recursos_interpostos', 0)))
                recursos_providos = st.number_input("Recursos providos", value=int(dados_semana_salvos.get('recursos_providos', 0)))
                recursos_improvidos = st.number_input("Recursos improvidos", value=int(dados_semana_salvos.get('recursos_improvidos', 0)))
                audiencias = st.number_input("Audiências realizadas", value=int(dados_semana_salvos.get('audiencias', 0)))
                pericias_judiciais = st.number_input("Perícias Judiciais agendadas", value=int(dados_semana_salvos.get('pericias_judiciais', 0)))
                pericias_jud_ausencias = st.number_input("Ausências em Perícias Judiciais", value=int(dados_semana_salvos.get('pericias_jud_ausencias', 0)))

                st.markdown("#### 📁 Operação Administrativa")
                processos_ativos_adm = st.number_input("Processos ativos administrativos", value=int(dados_semana_salvos.get('processos_ativos_adm', 0)))
                aguard_requerimento_adm = st.number_input("Estoque: Aguardando requerimentos", value=int(dados_semana_salvos.get('aguard_requerimento_adm', 0)))
                em_exigencia_adm = st.number_input("Estoque: Processos em exigência", value=int(dados_semana_salvos.get('em_exigencia_adm', 0)))
                
                req_adm = st.number_input("Requerimentos protocolados", value=int(dados_semana_salvos.get('req_adm', 0)))
                req_def = st.number_input("Requerimentos deferidos", value=int(dados_semana_salvos.get('req_def', 0)))
                req_indef = st.number_input("Requerimentos indeferidos", value=int(dados_semana_salvos.get('req_indef', 0)))
                desistencias_adm = st.number_input("Desistências no administrativo", value=int(dados_semana_salvos.get('desistencias_adm', 0)))
                pericias_adm = st.number_input("Perícias Administrativas agendadas", value=int(dados_semana_salvos.get('pericias_adm', 0)))
                pericias_adm_ausencias = st.number_input("Ausências em Perícias Adm.", value=int(dados_semana_salvos.get('pericias_adm_ausencias', 0)))

                st.markdown("#### ⭐ Qualidade & Satisfação")
                onboardings = st.number_input("Onboardings concluídos", value=int(dados_semana_salvos.get('onboardings', 0)))
                avaliacoes_google = st.number_input("Novas avaliações no Google", value=int(dados_semana_salvos.get('avaliacoes_google', 0)))
                reclamacoes = st.number_input("Reclamações formais", value=int(dados_semana_salvos.get('reclamacoes', 0)))
                cancelados_desistencia = st.number_input("Cancelados por Desistência", value=int(dados_semana_salvos.get('cancelados_desistencia', 0)))
                cancelados_docs_direito = st.number_input("Cancelados - Docs/Direito", value=int(dados_semana_salvos.get('cancelados_docs_direito', 0)))

            submitted = st.form_submit_button(f"💾 Salvar Dados da {semana_atual}")
            if submitted:
                st.session_state['base_dados_geral'][escritorio_selecionado][mes_ano_str][semana_atual] = {
                    'leads': leads, 'qualificados': qualificados, 'contratos': contratos, 'contratos_cancelados': contratos_cancelados,
                    'receita_contratada': receita_contratada, 'faturamento': faturamento, 'recebido': recebido, 'vencido': vencido, 
                    'rpv_precatorio': rpv_precatorio, 'pagamento_adm': pagamento_adm,
                    'advogados': advogados, 'estagiarios': estagiarios, 'auxiliares': auxiliares, 'assistentes': assistentes,
                    'clientes_aguard_judicial': clientes_aguard_judicial, 'clientes_aguard_adm': clientes_aguard_adm,
                    'processos_ativos_jud': processos_ativos_jud, 'aguard_revisao_jud': aguard_revisao_jud, 'aguard_protocolo_jud': aguard_protocolo_jud,
                    'protocolados_mes': protocolados_mes, 'protocolados_prazo_fatal': protocolados_prazo_fatal, 'emendas_inicial': emendas_inicial,
                    'sentecas_proc': sentecas_proc, 'sentecas_improc': sentecas_improc, 'extintos_sem_merito': extintos_sem_merito, 'desistencias_jud': desistencias_jud,
                    'recursos_interpostos': recursos_interpostos, 'recursos_providos': recursos_providos, 'recursos_improvidos': recursos_improvidos,
                    'audiencias': audiencias, 'pericias_judiciais': pericias_judiciais, 'pericias_jud_ausencias': pericias_jud_ausencias,
                    'processos_ativos_adm': processos_ativos_adm, 'aguard_requerimento_adm': aguard_requerimento_adm, 'em_exigencia_adm': em_exigencia_adm,
                    'req_adm': req_adm, 'req_def': req_def, 'req_indef': req_indef, 'desistencias_adm': desistencias_adm,
                    'pericias_adm': pericias_adm, 'pericias_adm_ausencias': pericias_adm_ausencias,
                    'reclamacoes': reclamacoes, 'avaliacoes_google': avaliacoes_google, 'onboardings': onboardings,
                    'cancelados_desistencia': cancelados_desistencia, 'cancelados_docs_direito': cancelados_docs_direito
                }
                st.success(f"Dados da **{semana_atual}** salvos para **{escritorio_selecionado}** ({mes_ano_str})!")
                st.rerun()

    # --- Consolidação ---
    totais_mes = {}
    chaves_numericas = [
        'leads', 'qualificados', 'contratos', 'contratos_cancelados', 'receita_contratada',
        'faturamento', 'recebido', 'vencido', 'rpv_precatorio', 'pagamento_adm', 'clientes_aguard_judicial', 'clientes_aguard_adm',
        'protocolados_mes', 'protocolados_prazo_fatal', 'emendas_inicial', 'sentecas_proc', 'sentecas_improc',
        'extintos_sem_merito', 'desistencias_jud', 'recursos_interpostos', 'recursos_providos', 'recursos_improvidos',
        'audiencias', 'pericias_judiciais', 'pericias_jud_ausencias', 'req_adm', 'req_def', 'req_indef',
        'desistencias_adm', 'pericias_adm', 'pericias_adm_ausencias', 'reclamacoes', 'avaliacoes_google', 'onboardings',
        'cancelados_desistencia', 'cancelados_docs_direito'
    ]
    chaves_estoque = ['processos_ativos_jud', 'aguard_revisao_jud', 'aguard_protocolo_jud', 'processos_ativos_adm', 'aguard_requerimento_adm', 'em_exigencia_adm', 'advogados', 'estagiarios', 'auxiliares', 'assistentes']

    for chave in chaves_numericas:
        totais_mes[chave] = sum([semana.get(chave, 0) for semana in historico_mes.values()])

    for chave in chaves_estoque:
        valor_recente = 0
        for sem in ["Semana 4", "Semana 3", "Semana 2", "Semana 1"]:
            if sem in historico_mes and historico_mes[sem].get(chave, 0) > 0:
                valor_recente = historico_mes[sem].get(chave, 0)
                break
        totais_mes[chave] = valor_recente

    taxa_conversao = (totais_mes['contratos'] / totais_mes['qualificados'] * 100) if totais_mes['qualificados'] > 0 else 0
    inadimplencia_pct = (totais_mes['vencido'] / totais_mes['faturamento'] * 100) if totais_mes['faturamento'] > 0 else 0
    total_aguardando = totais_mes['clientes_aguard_judicial'] + totais_mes['clientes_aguard_adm']
    total_entregue_protocolos = totais_mes['protocolados_mes'] + totais_mes['req_adm']

    if totais_mes['leads'] == 0 and totais_mes['contratos'] == 0 and totais_mes['faturamento'] == 0:
        score_geral = 0.0
    else:
        score_comercial = 84.0 if taxa_conversao >= 20 else 60.0
        score_financeiro = 68.0 if inadimplencia_pct < 10 else 50.0
        score_operacao = 51.0
        score_cliente = 78.0 if totais_mes['avaliacoes_google'] >= 5 else 60.0
        score_gestao = 74.0
        score_geral = (score_comercial * 0.20) + (score_financeiro * 0.20) + (score_operacao * 0.30) + (score_cliente * 0.15) + (score_gestao * 0.15)

    with tab2:
        st.header(f"Consolidado Mensal Amplo — {escritorio_selecionado} ({mes_ano_str})")
        st.markdown("Visão executiva integrada de todas as áreas do escritório no mês.")
        
        # Bloco 1: Visão Geral & Score
        c1, c2, c3, c4 = st.columns(4)
        status_score = "Aguardando Dados" if score_geral == 0 else "Consolidado"
        c1.metric("Score APO (Mensal)", f"{score_geral:.0f} / 100", status_score)
        c2.metric("Total Vendido (Contratos)", totais_mes['contratos'])
        c3.metric("Faturamento Consolidado", f"R$ {totais_mes['faturamento']:,.2f}")
        c4.metric("Recebido Efetivo", f"R$ {totais_mes['recebido']:,.2f}")

        st.markdown("---")
        
        # Bloco 2: Comercial & Financeiro Expandido
        st.subheader("💰 Comercial & Financeiro")
        f1, f2, f3, f4, f5 = st.columns(5)
        f1.metric("Leads / Qualificados", f"{totais_mes['leads']} / {totais_mes['qualificados']}")
        f2.metric("Taxa de Conversão", f"{taxa_conversao:.1f}%")
        f3.metric("Inadimplência", f"{inadimplencia_pct:.1f}%", f"R$ {totais_mes['vencido']:,.2f}")
        f4.metric("RPV / Precatório", f"R$ {totais_mes['rpv_precatorio']:,.2f}")
        f5.metric("Pagamento Administrativo", f"R$ {totais_mes['pagamento_adm']:,.2f}")

        st.markdown("---")

        # Bloco 3: Operação Judicial & Administrativa
        st.subheader("⚖️ Operação & Produção")
        o1, o2, o3, o4 = st.columns(4)
        o1.metric("Protocolos Judiciais (Mês)", totais_mes['protocolados_mes'], f"No prazo: {totais_mes['protocolados_prazo_fatal']}")
        o2.metric("Requerimentos Administrativos", totais_mes['req_adm'], f"Deferidos: {totais_mes['req_def']}")
        o3.metric("Sentenças (Proc. / Improc.)", f"{totais_mes['sentecas_proc']} / {totais_mes['sentecas_improc']}")
        o4.metric("Audiências & Perícias", f"{totais_mes['audiencias']} Aud / {totais_mes['pericias_judiciais']} Per")

        st.markdown("---")

        # Bloco 4: Equipe & Qualidade / Cancelamentos
        st.subheader("⭐ Equipe, Qualidade & Retenção")
        q1, q2, q3, q4, q5 = st.columns(5)
        q1.metric("Total Equipe", totais_mes['advogados'] + totais_mes['estagiarios'] + totais_mes['auxiliares'] + totais_mes['assistentes'], f"{totais_mes['advogados']} Adv / {totais_mes['estagiarios']} Estág")
        q2.metric("Onboardings", totais_mes['onboardings'])
        q3.metric("Avaliações Google", totais_mes['avaliacoes_google'])
        q4.metric("Cancelados (Desistência)", totais_mes['cancelados_desistencia'])
        q5.metric("Cancelados (Docs/Direito)", totais_mes['cancelados_docs_direito'])

        st.markdown("---")
        st.subheader("📊 Histórico Detalhado por Semana")
        df_semanas = pd.DataFrame(historico_mes).T
        st.dataframe(df_semanas, use_container_width=True)

    with tab3:
        st.header(f"Previsibilidade: Vendido vs. Entregue — {escritorio_selecionado}")
        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.metric("Total Vendido no Mês", totais_mes['contratos'])
        col_p2.metric("Total Entregue (Protocolos + Req)", total_entregue_protocolos, f"{totais_mes['protocolados_mes']} Jud / {totais_mes['req_adm']} Adm")
        
        indice_vazao = (total_entregue_protocolos / totais_mes['contratos'] * 100) if totais_mes['contratos'] > 0 else 0
        col_p3.metric("Índice de Vazão Mensal", f"{indice_vazao:.1f}%", "Meta: 100%")

    with tab4:
        st.header(f"Diagnóstico Geral — {escritorio_selecionado}")
        if score_geral == 0:
            st.info("Preencha as semanas para gerar o diagnóstico.")
        else:
            st.error("🚨 **PONTOS DE ATENÇÃO OPERACIONAL**")
            st.write(f"Há **{total_aguardando} clientes** na esteira e **{totais_mes['aguard_protocolo_jud']} processos** aguardando protocolo judicial.")

    with tab5:
        st.header("📋 Plano de Ação Estratégico")
        if score_geral == 0:
            st.info("Preencha as semanas para gerar o plano de ação.")
        else:
            st.markdown(f"* **Foco Semanal:** Zerar protocolo de {totais_mes['aguard_protocolo_jud']} itens.")
            st.markdown(f"* **Foco Mensal:** Tratar cancelamentos por desistência ({totais_mes['cancelados_desistencia']}) e docs/direito ({totais_mes['cancelados_docs_direito']}).")
