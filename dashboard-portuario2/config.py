"""
Configurações centralizadas para o Sistema Portuário
"""
import os
from typing import Dict, Any

# Configurações das APIs do Instituto AmiGU
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

# Configuração do n8n
N8N_CONFIG = {
    "webhook_url": "https://n8n.hackathon.souamigu.org.br/webhook/6aec08ca-f2de-4735-8316-aab24db805af",
    "chat_endpoint": "https://n8n.hackathon.souamigu.org.br/chat/288d383c-5e9c-4354-9dfa-9258f72def9f"
}

# Headers para autenticação
API_HEADERS = {
    "Authorization": f"ApiKey {os.getenv('AMIGU_API_KEY', 'YOUR_API_KEY_HERE')}",
    "Content-Type": "application/json"
}

# Configurações do OpenAI
OPENAI_CONFIG = {
    "api_key": os.getenv('OPENAI_API_KEY'),
    "model": "gpt-4o",
    "max_tokens": 1000,
    "temperature": 0.1
}

# Regras específicas do Porto de Santos
PORTO_SANTOS_RULES = {
    "DUE": {
        "required_fields": ["numero_due", "navio", "agente", "carga"],
        "format": "PDF",
        "max_size_mb": 10,
        "description": "Declaração Única de Exportação"
    },
    "Manifesto": {
        "required_fields": ["lista_carga", "origem", "destino", "peso"],
        "format": "PDF",
        "max_size_mb": 15,
        "description": "Manifesto de Carga"
    },
    "Certificado_Sanitario": {
        "required_fields": ["autoridade_sanitaria", "data_inspecao", "resultado"],
        "format": "PDF",
        "max_size_mb": 5,
        "description": "Certificado Sanitário ANVISA"
    },
    "Certificado_Seguranca": {
        "required_fields": ["validade", "autoridade_emissora", "tipo_certificado"],
        "format": "PDF",
        "max_size_mb": 5,
        "description": "Certificado de Segurança"
    },
    "Plano_Carga": {
        "required_fields": ["distribuicao_carga", "peso_total", "centro_gravidade"],
        "format": "PDF",
        "max_size_mb": 20,
        "description": "Plano de Carregamento"
    },
    "Autorizacao_IBAMA": {
        "required_fields": ["numero_licenca", "validade", "tipo_carga"],
        "format": "PDF",
        "max_size_mb": 5,
        "description": "Autorização Ambiental IBAMA"
    }
}

# Configurações do sistema
SYSTEM_CONFIG = {
    "max_file_size_mb": 25,
    "supported_formats": ["pdf"],
    "max_notifications": 10,
    "refresh_interval": 30,
    "ai_timeout": 30
}
