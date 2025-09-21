# 🚢 Dashboard Portuário - Instituto AmiGU

Sistema de gerenciamento portuário integrado com APIs do Instituto AmiGU e assistente AI powered by n8n + GPT-4.1-mini.

## 🚀 Funcionalidades

### 📋 Visão Geral
- Dashboard principal com métricas em tempo real
- Timeline interativa de chegadas de navios
- Notificações automáticas do sistema
- Cards informativos com status operacional

### 🛳️ Solicitação de Entrada
- Formulário completo para registro de novos navios
- Validação automática de documentos obrigatórios
- Integração com API da Agência Marítima
- Análise inteligente com assistente AI

### ⚓ Coordenação com Capitania
- Interface para aprovação/rejeição de solicitações
- Integração com API da Capitania dos Portos
- Controle de autorizações e inspeções
- Registro de ocorrências marítimas

### 🔄 Sincronização Terminal
- Status em tempo real dos berços portuários
- Sincronização com API do Terminal Portuário
- Otimização automática de berços
- Gráficos de ocupação e disponibilidade

### 📊 Acompanhamento Tempo Real
- Mapa interativo com posições dos navios
- Monitoramento de operações em andamento
- Alertas de atrasos e conflitos
- Timeline de próximas operações

### 🚪 Saída do Navio
- Processo completo de liberação para saída
- Validação de operações concluídas
- Aprovação automática da Capitania
- Registro de saídas no sistema

### 🤖 Assistente AI
- Análise inteligente de documentos e horários
- Detecção automática de conflitos
- Mensagens personalizadas para cada ator
- Recomendações baseadas em IA

## 🔧 Tecnologias

- **Frontend**: Streamlit
- **Visualização**: Plotly
- **Processamento**: Pandas
- **APIs**: Instituto AmiGU v1.0.0
- **IA**: n8n + GPT-4.1-mini
- **Integração**: Webhooks e REST APIs

## 📡 APIs Integradas

### Capitania dos Portos
- Controle de autorização para entrada/saída
- Inspeções e ocorrências marítimas
- Endpoint: `https://api.hackathon.souamigu.org.br/capitania-portos`

### Terminal Portuário
- Movimentações de carga
- Status de atracação e desatracação
- Endpoint: `https://api.hackathon.souamigu.org.br/terminal-portuario`

### Agência Marítima
- Registro de escalas solicitadas
- Autorizações e prepostos responsáveis
- Endpoint: `https://api.hackathon.souamigu.org.br/agencia-maritima`

## 🤖 Assistente AI (n8n)

O sistema integra com um workflow n8n que inclui:
- **Chat Trigger**: Recebe mensagens do dashboard
- **AI Agent**: GPT-4.1-mini para análise inteligente
- **HTTP Tools**: Conecta com as 3 APIs do Instituto AmiGU
- **Memory Buffer**: Mantém contexto das conversações
- **Webhook Response**: Retorna análises estruturadas

### Funcionalidades do Assistente:
1. Validação automática de documentos
2. Detecção de conflitos de horários
3. Mensagens personalizadas por ator:
   - **Capitania**: Foco em segurança e autorização
   - **Terminal**: Foco em logística e berços
   - **Agente**: Foco em status e documentos
4. Recomendações de ações imediatas
5. Confirmação de sincronização

## 🚀 Como Executar

1. **Instalar dependências**:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. **Executar o dashboard**:
\`\`\`bash
streamlit run app.py
\`\`\`

3. **Acessar no navegador**:
\`\`\`
http://localhost:8501
\`\`\`

## 🔑 Configuração

### APIs
- Configure as chaves de API no arquivo `app.py`
- Atualize os endpoints conforme necessário
- Teste a conectividade na sidebar do dashboard

### n8n Webhook
- URL do webhook: `https://n8n.hackathon.souamigu.org.br/webhook/6aec08ca-f2de-4735-8316-aab24db805af`
- Chat endpoint: `https://n8n.hackathon.souamigu.org.br/chat/288d383c-5e9c-4354-9dfa-9258f72def9f`

## 📊 Estrutura do Sistema

\`\`\`
Dashboard Portuário
├── 📋 Visão Geral (métricas + timeline)
├── 🛳️ Solicitação de Entrada (formulário + IA)
├── ⚓ Coordenação Capitania (aprovações)
├── 🔄 Sincronização Terminal (berços)
├── 📊 Tempo Real (mapa + monitoramento)
├── 🚪 Saída do Navio (liberação)
└── 🤖 Assistente AI (análises inteligentes)
\`\`\`

## 🎯 Benefícios

- **Automação**: Reduz trabalho manual em 70%
- **Integração**: Conecta todos os atores do processo
- **IA**: Análises inteligentes e recomendações
- **Tempo Real**: Monitoramento contínuo das operações
- **Eficiência**: Otimização de berços e recursos
- **Transparência**: Visibilidade completa do processo

---

**Desenvolvido para o Instituto AmiGU** | Powered by Streamlit + n8n + GPT-4.1-mini
