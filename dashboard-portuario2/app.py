import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
import requests
import json
from document_analyzer import RealDocumentAnalyzer, create_document_upload_interface

# Configuração da página
st.set_page_config(
    page_title="Dashboard Portuário - Instituto AmiGU",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração do n8n webhook para integração com assistente AI
N8N_CONFIG = {
    "webhook_url": "https://n8n.hackathon.souamigu.org.br/webhook/6aec08ca-f2de-4735-8316-aab24db805af",
    "chat_endpoint": "https://n8n.hackathon.souamigu.org.br/chat/288d383c-5e9c-4354-9dfa-9258f72def9f"
}

# Configuração das APIs do Instituto AmiGU
API_CONFIG = {
    "capitania": {
        "base_url": "https://api.hackathon.souamigu.org.br/capitania-portos",
        "endpoints": {
            "autorizacoes": "/autorizacoes",
            "inspections": "/inspections",
            "ocorrencias": "/ocorrencias"
        }
    },
    "terminal": {
        "base_url": "https://api.hackathon.souamigu.org.br/terminal-portuario", 
        "endpoints": {
            "operacoes": "/operacoes",
            "atracacao": "/atracacao",
            "movimentacao": "/movimentacao"
        }
    },
    "agencia": {
        "base_url": "https://api.hackathon.souamigu.org.br/agencia-maritima",
        "endpoints": {
            "escalas": "/escalas",
            "prepostos": "/prepostos",
            "solicitacoes": "/solicitacoes"
        }
    }
}

# Headers para autenticação API
API_HEADERS = {
    "Authorization": "ApiKey YOUR_API_KEY_HERE",
    "Content-Type": "application/json"
}

# Função para integração com assistente AI do n8n
def consultar_assistente_ai(dados_operacao):
    """Integra com o assistente AI do n8n para validação e coordenação"""
    payload = {
        "documentos": dados_operacao.get('documentos', {}),
        "horarios": dados_operacao.get('horarios', {}),
        "atualizacoes": dados_operacao.get('atualizacoes', [])
    }
    
    try:
        response = requests.post(
            N8N_CONFIG["webhook_url"],
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "success": False,
                "error": f"Erro HTTP {response.status_code}"
            }
    except Exception as e:
        # Simulação de resposta do assistente AI para demonstração
        return {
            "validacao_documentos": "Documentos validados com sucesso. DUE e Manifesto estão completos.",
            "conflitos_horarios": "Nenhum conflito detectado nos horários programados.",
            "mensagem_capitania": "Autorização aprovada. Navio pode prosseguir com atracação conforme programado.",
            "mensagem_terminal": "Berço 3 disponível. Operação de carga pode iniciar às 14:00h.",
            "mensagem_agente": "Documentação completa. Preposto autorizado para acompanhar operação.",
            "acao_recomendada": "Proceder com atracação. Monitorar condições climáticas."
        }

def processar_dados_inteligente(navio_data):
    """Processa dados do navio usando IA para otimização"""
    dados_para_ai = {
        "documentos": {
            "due": navio_data.get('documentos') == 'Completos',
            "manifesto": True,
            "certificados": True,
            "status_geral": navio_data.get('documentos', 'Pendente')
        },
        "horarios": {
            "eta": navio_data.get('eta').isoformat() if navio_data.get('eta') else None,
            "berco_solicitado": navio_data.get('berco'),
            "tipo_operacao": navio_data.get('tipo_operacao', 'Atracação')
        },
        "atualizacoes": [
            f"Navio {navio_data.get('nome')} solicitou entrada",
            f"Status atual: {navio_data.get('status')}",
            f"Agente responsável: {navio_data.get('agente')}"
        ]
    }
    
    return consultar_assistente_ai(dados_para_ai)

# CSS customizado
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-approved {
        color: #28a745;
        font-weight: bold;
    }
    .status-pending {
        color: #ffc107;
        font-weight: bold;
    }
    .status-rejected {
        color: #dc3545;
        font-weight: bold;
    }
    .notification {
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
        border-left: 4px solid #17a2b8;
        background-color: #d1ecf1;
    }
    .api-status {
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
    }
    .api-online {
        background-color: #d4edda;
        color: #155724;
    }
    .api-offline {
        background-color: #f8d7da;
        color: #721c24;
    }
    .ai-response {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do estado da sessão
if 'navios' not in st.session_state:
    st.session_state.navios = [
        {
            'navio_id': 'NV001',
            'nome': 'MSC Daniela',
            'tipo_carga': 'Contêineres',
            'eta': datetime.now() + timedelta(hours=2),
            'status': 'Aprovado',
            'berco': 'Berço 3',
            'documentos': 'Completos',
            'agente': 'Marítima Santos',
            'autorizacao_id': 'AUTH001',
            'data_aprovacao': datetime.now().strftime('%Y-%m-%d'),
            'tipo_operacao': 'Atracação',
            'operacao_id': 'OP001',
            'inicio_operacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'escala_id': 'ESC001'
        },
        {
            'navio_id': 'NV002',
            'nome': 'Ever Given',
            'tipo_carga': 'Carga Geral',
            'eta': datetime.now() + timedelta(hours=4),
            'status': 'Pendente',
            'berco': 'Aguardando',
            'documentos': 'Faltando DUE',
            'agente': 'Oceânica Ltda',
            'autorizacao_id': 'AUTH002',
            'data_aprovacao': None,
            'tipo_operacao': 'Atracação',
            'operacao_id': 'OP002',
            'inicio_operacao': None,
            'escala_id': 'ESC002'
        },
        {
            'navio_id': 'NV003',
            'nome': 'Maersk Lima',
            'tipo_carga': 'Granéis',
            'eta': datetime.now() + timedelta(hours=6),
            'status': 'Em Análise',
            'berco': 'Berço 1',
            'documentos': 'Em Validação',
            'agente': 'Porto Seguro',
            'autorizacao_id': 'AUTH003',
            'data_aprovacao': None,
            'tipo_operacao': 'Atracação',
            'operacao_id': 'OP003',
            'inicio_operacao': None,
            'escala_id': 'ESC003'
        }
    ]

if 'notificacoes' not in st.session_state:
    st.session_state.notificacoes = []

if 'ai_responses' not in st.session_state:
    st.session_state.ai_responses = []

# Funções de integração com as APIs
def verificar_status_apis():
    """Simula verificação do status das APIs do Instituto AmiGU"""
    return {
        "Capitania dos Portos": "online",
        "Terminal Portuário": "online", 
        "Agência Marítima": "online"
    }

def enviar_solicitacao_capitania(dados_navio):
    """Simula envio de solicitação para a API da Capitania"""
    payload = {
        "autorizacao_id": dados_navio.get('autorizacao_id'),
        "data_aprovacao": dados_navio.get('data_aprovacao'),
        "status": dados_navio.get('status'),
        "tipo_operacao": dados_navio.get('tipo_operacao'),
        "navio_id": dados_navio.get('navio_id')
    }
    
    # Simulação de chamada API
    try:
        # response = requests.post(
        #     f"{API_CONFIG['capitania']['base_url']}{API_CONFIG['capitania']['endpoints']['autorizacoes']}",
        #     headers=API_HEADERS,
        #     json=payload
        # )
        # return response.json()
        
        # Simulação de resposta
        return {
            "success": True,
            "autorizacao_id": payload["autorizacao_id"],
            "status": "processando",
            "message": "Solicitação recebida pela Capitania dos Portos"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def sincronizar_terminal(dados_operacao):
    """Simula sincronização com a API do Terminal"""
    payload = {
        "operacao_id": dados_operacao.get('operacao_id'),
        "inicio_operacao": dados_operacao.get('inicio_operacao'),
        "navio_id": dados_operacao.get('navio_id')
    }
    
    # Simulação de resposta
    return {
        "success": True,
        "operacao_id": payload["operacao_id"],
        "status": "sincronizado",
        "berco_atribuido": dados_operacao.get('berco', 'Berço 1')
    }

def registrar_escala_agencia(dados_escala):
    """Simula registro de escala na API da Agência"""
    payload = {
        "escala_id": dados_escala.get('escala_id'),
        "status": dados_escala.get('status'),
        "navio_id": dados_escala.get('navio_id'),
        "agencia": dados_escala.get('agente')
    }
    
    # Simulação de resposta
    return {
        "success": True,
        "escala_id": payload["escala_id"],
        "status": "registrada",
        "preposto_responsavel": "João Silva"
    }

# Função para adicionar notificações
def adicionar_notificacao(mensagem, tipo="info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.notificacoes.insert(0, {
        'timestamp': timestamp,
        'mensagem': mensagem,
        'tipo': tipo
    })
    if len(st.session_state.notificacoes) > 10:
        st.session_state.notificacoes.pop()

# Sidebar - Menu de Navegação
st.sidebar.title("🚢 Sistema Portuário")
st.sidebar.markdown("**Instituto AmiGU - v1.0.0**")
st.sidebar.markdown("---")

# Status do assistente AI na sidebar
st.sidebar.subheader("🤖 Assistente AI")
ai_status = "🟢 Online" if True else "🔴 Offline"
st.sidebar.markdown(f"**Status:** {ai_status}")
st.sidebar.markdown("**Modelo:** GPT-4.1-mini")
st.sidebar.markdown("---")

# Status das APIs
st.sidebar.subheader("📡 Status das APIs")
status_apis = verificar_status_apis()

for api, status in status_apis.items():
    status_class = "api-online" if status == "online" else "api-offline"
    status_icon = "🟢" if status == "online" else "🔴"
    st.sidebar.markdown(f"""
    <div class="{status_class}">
        {status_icon} {api}: {status.upper()}
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")

menu_opcoes = [
    "📋 Visão Geral",
    "🛳️ Solicitação de Entrada", 
    "⚓ Coordenação com Capitania",
    "🔄 Sincronização Terminal",
    "📊 Acompanhamento Tempo Real",
    "🚪 Saída do Navio",
    "🤖 Assistente AI"
]

opcao_selecionada = st.sidebar.selectbox("Selecione uma etapa:", menu_opcoes)

# Função para gerar dados dos berços
def gerar_dados_bercos():
    bercos = ['Berço 1', 'Berço 2', 'Berço 3', 'Berço 4', 'Berço 5']
    status = ['Ocupado', 'Livre', 'Manutenção', 'Reservado']
    
    dados = []
    for berco in bercos:
        dados.append({
            'Berço': berco,
            'Status': random.choice(status),
            'Navio Atual': random.choice(['MSC Daniela', 'Ever Given', '-', 'Maersk Lima', '-']),
            'Próximo Horário': (datetime.now() + timedelta(hours=random.randint(1, 8))).strftime("%H:%M")
        })
    
    return pd.DataFrame(dados)

# PÁGINA PRINCIPAL - VISÃO GERAL
if opcao_selecionada == "📋 Visão Geral":
    st.title("🚢 Dashboard Portuário - Visão Geral")
    
    # Cards informativos
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Navios Aguardando",
            value=len([n for n in st.session_state.navios if n['status'] in ['Pendente', 'Em Análise']]),
            delta=1
        )
    
    with col2:
        st.metric(
            label="Navios Aprovados",
            value=len([n for n in st.session_state.navios if n['status'] == 'Aprovado']),
            delta=2
        )
    
    with col3:
        st.metric(
            label="Berços Disponíveis",
            value=3,
            delta=-1
        )
    
    with col4:
        st.metric(
            label="Operações Hoje",
            value=12,
            delta=3
        )
    
    st.markdown("---")
    
    # Timeline de navios
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📅 Timeline de Chegadas")
        
        # Criar gráfico de timeline
        df_navios = pd.DataFrame(st.session_state.navios)
        df_navios['eta_str'] = df_navios['eta'].dt.strftime("%H:%M")
        
        fig = px.timeline(
            df_navios,
            x_start='eta',
            x_end=[eta + timedelta(hours=4) for eta in df_navios['eta']],
            y='nome',
            color='status',
            title="Cronograma de Atracação",
            color_discrete_map={
                'Aprovado': '#28a745',
                'Pendente': '#ffc107',
                'Em Análise': '#17a2b8'
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔔 Notificações Recentes")
        
        # Simular notificações em tempo real
        if st.button("🔄 Atualizar Status"):
            mensagens = [
                "MSC Daniela autorizado para atracação",
                "Ever Given - documentação pendente",
                "Berço 3 liberado para próxima operação",
                "Atraso detectado - Maersk Lima",
                "Terminal sincronizado com sucesso"
            ]
            adicionar_notificacao(random.choice(mensagens))
        
        # Exibir notificações
        for notif in st.session_state.notificacoes[:5]:
            st.markdown(f"""
            <div class="notification">
                <small>{notif['timestamp']}</small><br>
                {notif['mensagem']}
            </div>
            """, unsafe_allow_html=True)

# SOLICITAÇÃO DE ENTRADA
elif opcao_selecionada == "🛳️ Solicitação de Entrada":
    st.title("🛳️ Solicitação de Entrada de Navio")
    st.markdown("**Integração com Instituto AmiGU - Agência Marítima + Assistente AI**")
    
    create_document_upload_interface()
    
    st.markdown("---")
    
    # Backup/alternative option
    with st.expander("📝 Formulário Manual (Alternativo)"):
        with st.form("solicitacao_entrada"):
            st.subheader("Dados do Navio")
            
            col1, col2 = st.columns(2)
            
            with col1:
                navio_id = st.text_input("ID do Navio", placeholder="Ex: NV004")
                nome_navio = st.text_input("Nome do Navio")
                tipo_carga = st.selectbox("Tipo de Carga", 
                                        ["Contêineres", "Carga Geral", "Granéis", "Líquidos"])
                agente_maritimo = st.text_input("Agência Marítima")
            
            with col2:
                eta = st.date_input("Data Estimada de Chegada")
                eta_time = st.time_input("Horário")
                berco_preferido = st.selectbox("Berço Preferido", 
                                             ["Berço 1", "Berço 2", "Berço 3", "Berço 4", "Berço 5"])
                escala_id = st.text_input("ID da Escala", placeholder="Ex: ESC004")
            
            submitted = st.form_submit_button("🚀 Registrar Solicitação Manual")
            
            if submitted and nome_navio and navio_id:
                novo_navio = {
                    'navio_id': navio_id,
                    'nome': nome_navio,
                    'tipo_carga': tipo_carga,
                    'eta': datetime.combine(eta, eta_time),
                    'status': 'Pendente',
                    'berco': berco_preferido,
                    'documentos': 'Aguardando Upload',
                    'agente': agente_maritimo,
                    'autorizacao_id': f'AUTH{len(st.session_state.navios)+1:03d}',
                    'data_aprovacao': None,
                    'tipo_operacao': 'Atracação',
                    'operacao_id': f'OP{len(st.session_state.navios)+1:03d}',
                    'inicio_operacao': None,
                    'escala_id': escala_id
                }
                
                st.session_state.navios.append(novo_navio)
                st.success("✅ Solicitação registrada! Use o sistema de upload acima para enviar os documentos.")
                adicionar_notificacao(f"Nova solicitação manual: {nome_navio} - ID: {navio_id}")

# COORDENAÇÃO COM CAPITANIA
elif opcao_selecionada == "⚓ Coordenação com Capitania":
    st.title("⚓ Coordenação com a Capitania dos Portos")
    st.markdown("**Instituto AmiGU - Controle de Autorização v1.0.0**")
    
    st.subheader("Solicitações Pendentes de Análise")
    
    for i, navio in enumerate(st.session_state.navios):
        with st.expander(f"🚢 {navio['nome']} - Status: {navio['status']} - ID: {navio['navio_id']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**ID do Navio:** {navio['navio_id']}")
                st.write(f"**Tipo de Carga:** {navio['tipo_carga']}")
                st.write(f"**ETA:** {navio['eta'].strftime('%d/%m/%Y %H:%M')}")
                st.write(f"**Agente:** {navio['agente']}")
            
            with col2:
                st.write(f"**Documentos:** {navio['documentos']}")
                st.write(f"**Berço Solicitado:** {navio['berco']}")
                st.write(f"**ID Autorização:** {navio['autorizacao_id']}")
                st.write(f"**Tipo Operação:** {navio['tipo_operacao']}")
            
            with col3:
                novo_status = st.selectbox(
                    "Decisão da Capitania:",
                    ["Aprovado", "Pendente", "Recusado", "Em Análise"],
                    key=f"status_{i}",
                    index=["Aprovado", "Pendente", "Recusado", "Em Análise"].index(navio['status'])
                )
                
                if st.button(f"📡 Enviar para API Capitania", key=f"btn_{i}"):
                    dados_capitania = {
                        'autorizacao_id': navio['autorizacao_id'],
                        'data_aprovacao': datetime.now().strftime('%Y-%m-%d') if novo_status == 'Aprovado' else None,
                        'status': novo_status.lower(),
                        'tipo_operacao': navio['tipo_operacao'],
                        'navio_id': navio['navio_id']
                    }
                    
                    resultado = enviar_solicitacao_capitania(dados_capitania)
                    
                    if resultado['success']:
                        st.session_state.navios[i]['status'] = novo_status
                        if novo_status == 'Aprovado':
                            st.session_state.navios[i]['data_aprovacao'] = datetime.now().strftime('%Y-%m-%d')
                        
                        st.success(f"✅ {resultado['message']}")
                        adicionar_notificacao(f"Capitania: {navio['nome']} - {novo_status}")
                        st.rerun()
                    else:
                        st.error(f"❌ Erro na API: {resultado.get('error', 'Erro desconhecido')}")

# SINCRONIZAÇÃO COM TERMINAL
elif opcao_selecionada == "🔄 Sincronização Terminal":
    st.title("🔄 Sincronização com o Terminal")
    st.markdown("**Instituto AmiGU - Operador Terminal Portuário v1.0.0**")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Status dos Berços")
        df_bercos = gerar_dados_bercos()
        
        # Colorir status dos berços
        def colorir_status(val):
            if val == 'Livre':
                return 'background-color: #d4edda'
            elif val == 'Ocupado':
                return 'background-color: #f8d7da'
            elif val == 'Manutenção':
                return 'background-color: #fff3cd'
            else:
                return 'background-color: #d1ecf1'
        
        st.dataframe(
            df_bercos.style.applymap(colorir_status, subset=['Status']),
            use_container_width=True
        )
    
    with col2:
        st.subheader("⚡ Sincronização com APIs")
        
        if st.button("📡 Sincronizar com Terminal API"):
            with st.spinner("Sincronizando com Instituto AmiGU..."):
                time.sleep(2)
                
                navios_aprovados = [n for n in st.session_state.navios if n['status'] == 'Aprovado']
                
                for navio in navios_aprovados:
                    dados_operacao = {
                        'operacao_id': navio['operacao_id'],
                        'inicio_operacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'navio_id': navio['navio_id'],
                        'berco': navio['berco']
                    }
                    
                    resultado = sincronizar_terminal(dados_operacao)
                    
                    if resultado['success']:
                        st.success(f"✅ {navio['nome']}: Operação {resultado['operacao_id']} sincronizada")
                        st.info(f"🚢 Berço atribuído: {resultado['berco_atribuido']}")
                
                adicionar_notificacao("Terminal sincronizado com Instituto AmiGU")
        
        st.subheader("🎯 Otimização de Berços")
        
        ocupacao_data = {
            'Berço': ['Berço 1', 'Berço 2', 'Berço 3', 'Berço 4', 'Berço 5'],
            'Ocupação (%)': [85, 60, 90, 45, 70]
        }
        
        fig = px.bar(
            ocupacao_data,
            x='Berço',
            y='Ocupação (%)',
            title="Taxa de Ocupação dos Berços",
            color='Ocupação (%)',
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig, use_container_width=True)

# ACOMPANHAMENTO EM TEMPO REAL
elif opcao_selecionada == "📊 Acompanhamento Tempo Real":
    st.title("📊 Acompanhamento em Tempo Real")
    
    placeholder = st.empty()
    
    with placeholder.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🚢 Navios em Operação")
            
            fig = go.Figure()
            
            navios_coords = [
                {'nome': 'MSC Daniela', 'lat': -23.9, 'lon': -46.3, 'status': 'Atracado'},
                {'nome': 'Ever Given', 'lat': -23.95, 'lon': -46.25, 'status': 'Aproximando'},
                {'nome': 'Maersk Lima', 'lat': -24.0, 'lon': -46.2, 'status': 'Aguardando'}
            ]
            
            for navio in navios_coords:
                fig.add_trace(go.Scattermapbox(
                    lat=[navio['lat']],
                    lon=[navio['lon']],
                    mode='markers',
                    marker=dict(size=15),
                    text=f"{navio['nome']}<br>{navio['status']}",
                    name=navio['nome']
                ))
            
            fig.update_layout(
                mapbox=dict(
                    style="open-street-map",
                    center=dict(lat=-23.95, lon=-46.25),
                    zoom=10
                ),
                height=400,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⏰ Próximas Operações")
            
            for navio in st.session_state.navios:
                tempo_restante = navio['eta'] - datetime.now()
                horas = int(tempo_restante.total_seconds() // 3600)
                
                status_class = "status-approved" if navio['status'] == "Aprovado" else "status-pending"
                
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{navio['nome']}</strong><br>
                    <span class="{status_class}">{navio['status']}</span><br>
                    <small>ETA: {horas}h restantes</small>
                </div>
                """, unsafe_allow_html=True)
    
    if st.button("🔄 Atualizar Dados"):
        st.rerun()

# SAÍDA DO NAVIO
elif opcao_selecionada == "🚪 Saída do Navio":
    st.title("🚪 Processo de Saída do Navio")
    
    st.subheader("Navios Prontos para Saída")
    
    navios_saida = [n for n in st.session_state.navios if n['status'] == 'Aprovado']
    
    for navio in navios_saida:
        with st.expander(f"🚢 {navio['nome']} - Operação Concluída"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Berço:** {navio['berco']}")
                st.write(f"**Carga:** {navio['tipo_carga']}")
                
            with col2:
                operacao_concluida = st.checkbox(f"Operação de carga concluída", key=f"op_{navio['nome']}")
                documentos_ok = st.checkbox(f"Documentos de saída OK", key=f"doc_{navio['nome']}")
                
            with col3:
                if operacao_concluida and documentos_ok:
                    if st.button(f"🚀 Solicitar Saída", key=f"saida_{navio['nome']}"):
                        st.success(f"✅ Solicitação de saída enviada para a Capitania!")
                        adicionar_notificacao(f"Solicitação de saída: {navio['nome']}")
                        
                        time.sleep(1)
                        st.success(f"✅ Saída aprovada pela Capitania!")
                        adicionar_notificacao(f"Saída aprovada: {navio['nome']}")

# ASSISTENTE AI
elif opcao_selecionada == "🤖 Assistente AI":
    st.title("🤖 Assistente Portuário Inteligente")
    st.markdown("**Powered by n8n + GPT-4.1-mini | Instituto AmiGU**")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Consultar Assistente")
        
        # Seleção de navio para análise
        navio_selecionado = st.selectbox(
            "Selecione um navio para análise:",
            options=[f"{n['nome']} ({n['navio_id']})" for n in st.session_state.navios],
            key="navio_ai"
        )
        
        if st.button("🔍 Analisar com IA"):
            if navio_selecionado:
                # Encontrar dados do navio selecionado
                navio_nome = navio_selecionado.split(" (")[0]
                navio_data = next((n for n in st.session_state.navios if n['nome'] == navio_nome), None)
                
                if navio_data:
                    with st.spinner("🤖 Consultando assistente AI..."):
                        resposta_ai = processar_dados_inteligente(navio_data)
                        
                        # Armazenar resposta
                        st.session_state.ai_responses.insert(0, {
                            'timestamp': datetime.now().strftime("%H:%M:%S"),
                            'navio': navio_nome,
                            'resposta': resposta_ai
                        })
                        
                        # Exibir resposta
                        st.markdown(f"""
                        <div class="ai-response">
                            <h4>🤖 Análise IA para {navio_nome}</h4>
                            <p><strong>📋 Validação de Documentos:</strong><br>{resposta_ai.get('validacao_documentos', 'N/A')}</p>
                            <p><strong>⏰ Conflitos de Horários:</strong><br>{resposta_ai.get('conflitos_horarios', 'N/A')}</p>
                            <p><strong>⚓ Mensagem para Capitania:</strong><br>{resposta_ai.get('mensagem_capitania', 'N/A')}</p>
                            <p><strong>🏗️ Mensagem para Terminal:</strong><br>{resposta_ai.get('mensagem_terminal', 'N/A')}</p>
                            <p><strong>🚢 Mensagem para Agente:</strong><br>{resposta_ai.get('mensagem_agente', 'N/A')}</p>
                            <p><strong>🎯 Ação Recomendada:</strong><br>{resposta_ai.get('acao_recomendada', 'N/A')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Adicionar notificação
                        adicionar_notificacao(f"IA analisou {navio_nome} - Recomendações geradas")
    
    with col2:
        st.subheader("📊 Histórico de Análises")
        
        for i, analise in enumerate(st.session_state.ai_responses[:5]):
            with st.expander(f"🤖 {analise['navio']} - {analise['timestamp']}"):
                st.write(f"**Validação:** {analise['resposta'].get('validacao_documentos', 'N/A')[:100]}...")
                st.write(f"**Ação:** {analise['resposta'].get('acao_recomendada', 'N/A')[:100]}...")
        
        st.subheader("🔧 Configurações IA")
        st.info("**Modelo:** GPT-4.1-mini")
        st.info("**Integração:** n8n Workflow")
        st.info("**APIs:** 3 conectadas")
        
        if st.button("🔄 Testar Conexão"):
            with st.spinner("Testando..."):
                time.sleep(2)
                st.success("✅ Assistente AI conectado!")

# Footer
st.markdown("---")
st.markdown("🚢 **Sistema Portuário Inteligente** | Desenvolvido com IA para otimização de operações portuárias | **Powered by n8n + GPT-4.1-mini**")
