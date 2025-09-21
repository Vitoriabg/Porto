# 🚢 Instalação do Sistema Portuário

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conta OpenAI com API Key (para análise de documentos)

## Instalação

### 1. Clone ou baixe o projeto
\`\`\`bash
# Se usando Git
git clone <repository-url>
cd dashboard-portuario

# Ou baixe o ZIP e extraia
\`\`\`

### 2. Instale as dependências
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

\`\`\`env
# OpenAI API Key (obrigatório para análise de documentos)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Instituto AmiGU API Key (opcional - para produção)
AMIGU_API_KEY=your-amigu-api-key-here

# Configurações opcionais
MAX_FILE_SIZE_MB=25
AI_TIMEOUT=30
\`\`\`

### 4. Execute o sistema
\`\`\`bash
streamlit run app.py
\`\`\`

## Funcionalidades Principais

### 📄 Upload e Análise de Documentos
- Upload de PDFs com validação automática
- Análise por IA usando GPT-4 Vision
- Verificação de conformidade com regras do Porto de Santos
- Extração de texto e análise de conteúdo

### 🤖 Assistente AI
- Integração com n8n workflow
- Análise inteligente de operações portuárias
- Recomendações automáticas
- Coordenação entre múltiplos atores

### 📡 Integração com APIs
- Capitania dos Portos
- Terminal Portuário
- Agência Marítima
- Sincronização em tempo real

## Configuração da OpenAI API

1. Acesse [platform.openai.com](https://platform.openai.com)
2. Crie uma conta ou faça login
3. Vá em "API Keys" e crie uma nova chave
4. Adicione a chave no arquivo `.env`

**Importante:** Mantenha sua API key segura e nunca a compartilhe publicamente.

## Estrutura do Projeto

\`\`\`
dashboard-portuario/
├── app.py                 # Aplicação principal Streamlit
├── document_analyzer.py   # Sistema de análise de documentos
├── config.py             # Configurações centralizadas
├── requirements.txt      # Dependências Python
├── README.md            # Documentação principal
├── INSTALL.md           # Guia de instalação
└── .env                 # Variáveis de ambiente (criar)
\`\`\`

## Solução de Problemas

### Erro: "No module named 'pdfplumber'"
\`\`\`bash
pip install pdfplumber
\`\`\`

### Erro: "OpenAI API key not found"
- Verifique se o arquivo `.env` existe
- Confirme se a variável `OPENAI_API_KEY` está definida
- Reinicie o Streamlit após adicionar a chave

### Erro de upload de arquivo
- Verifique se o arquivo é PDF
- Confirme se o tamanho é menor que 25MB
- Tente com um arquivo diferente

### Performance lenta na análise
- Verifique sua conexão com internet
- A análise por IA pode levar 10-30 segundos
- Arquivos grandes demoram mais para processar

## Suporte

Para problemas técnicos:
1. Verifique os logs no terminal
2. Confirme se todas as dependências estão instaladas
3. Teste com arquivos menores primeiro
4. Verifique se a OpenAI API key está válida

## Próximos Passos

Após a instalação:
1. Configure sua OpenAI API key
2. Teste o upload de um documento PDF
3. Explore as diferentes seções do dashboard
4. Configure as integrações com APIs reais (opcional)
