import base64
import io
import json
import requests
from typing import Dict, List, Any
import pdfplumber
from PIL import Image
import pdf2image
import openai
import streamlit as st

class RealDocumentAnalyzer:
    """Analisador real de documentos portuários usando IA"""
    
    def __init__(self, openai_api_key: str):
        self.client = openai.OpenAI(api_key=openai_api_key)
        
        # Regras específicas do Porto de Santos
        self.porto_santos_rules = {
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
            }
        }
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extrai texto do PDF usando pdfplumber"""
        try:
            text = ""
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            st.error(f"Erro ao extrair texto do PDF: {str(e)}")
            return ""
    
    def convert_pdf_to_images(self, pdf_file) -> List[Image.Image]:
        """Converte PDF em imagens para análise visual"""
        try:
            # Salva temporariamente o arquivo
            with open("temp_pdf.pdf", "wb") as f:
                f.write(pdf_file.getvalue())
            
            # Converte para imagens
            images = pdf2image.convert_from_path("temp_pdf.pdf", dpi=200)
            return images
        except Exception as e:
            st.error(f"Erro ao converter PDF para imagens: {str(e)}")
            return []
    
    def encode_image_to_base64(self, image: Image.Image) -> str:
        """Codifica imagem para base64"""
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    def analyze_document_with_ai(self, document_type: str, text_content: str, images: List[Image.Image]) -> Dict[str, Any]:
        """Analisa documento usando GPT-4 Vision"""
        try:
            rules = self.porto_santos_rules.get(document_type, {})
            
            # Prepara o prompt específico para o tipo de documento
            prompt = f"""
            Analise este documento portuário do tipo {document_type} ({rules.get('description', '')}).
            
            Regras do Porto de Santos para este documento:
            - Campos obrigatórios: {rules.get('required_fields', [])}
            - Formato: {rules.get('format', 'PDF')}
            - Tamanho máximo: {rules.get('max_size_mb', 10)}MB
            
            Texto extraído do documento:
            {text_content[:2000]}...
            
            Por favor, analise e retorne um JSON com:
            1. "valido": true/false
            2. "campos_encontrados": lista dos campos obrigatórios encontrados
            3. "campos_faltantes": lista dos campos obrigatórios não encontrados
            4. "observacoes": lista de observações sobre o documento
            5. "score_conformidade": pontuação de 0 a 100
            6. "recomendacoes": lista de recomendações para correção
            """
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ]
                }
            ]
            
            # Adiciona imagens se disponíveis
            if images:
                for i, image in enumerate(images[:3]):  # Máximo 3 páginas
                    base64_image = self.encode_image_to_base64(image)
                    messages[0]["content"].append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    })
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1000,
                temperature=0.1
            )
            
            # Tenta extrair JSON da resposta
            response_text = response.choices[0].message.content
            try:
                # Procura por JSON na resposta
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = response_text[start:end]
                    return json.loads(json_str)
            except:
                pass
            
            # Se não conseguir extrair JSON, retorna análise básica
            return {
                "valido": "aprovado" in response_text.lower(),
                "campos_encontrados": [],
                "campos_faltantes": rules.get('required_fields', []),
                "observacoes": [response_text[:200] + "..."],
                "score_conformidade": 50,
                "recomendacoes": ["Revisar documento conforme regras do porto"]
            }
            
        except Exception as e:
            st.error(f"Erro na análise por IA: {str(e)}")
            return {
                "valido": False,
                "campos_encontrados": [],
                "campos_faltantes": rules.get('required_fields', []),
                "observacoes": [f"Erro na análise: {str(e)}"],
                "score_conformidade": 0,
                "recomendacoes": ["Verificar documento e tentar novamente"]
            }
    
    def validate_file_format(self, file, document_type: str) -> Dict[str, Any]:
        """Valida formato e tamanho do arquivo"""
        rules = self.porto_santos_rules.get(document_type, {})
        
        validation = {
            "formato_valido": file.type == "application/pdf",
            "tamanho_valido": file.size <= (rules.get('max_size_mb', 10) * 1024 * 1024),
            "tamanho_mb": round(file.size / (1024 * 1024), 2),
            "tipo_arquivo": file.type
        }
        
        return validation
    
    def process_document(self, file, document_type: str) -> Dict[str, Any]:
        """Processa documento completo"""
        
        # 1. Validação básica
        file_validation = self.validate_file_format(file, document_type)
        
        if not file_validation["formato_valido"]:
            return {
                "status": "erro",
                "mensagem": "Formato de arquivo inválido. Apenas PDF é aceito.",
                "detalhes": file_validation
            }
        
        if not file_validation["tamanho_valido"]:
            return {
                "status": "erro", 
                "mensagem": f"Arquivo muito grande. Máximo: {self.porto_santos_rules[document_type]['max_size_mb']}MB",
                "detalhes": file_validation
            }
        
        # 2. Extração de texto
        text_content = self.extract_text_from_pdf(file)
        
        # 3. Conversão para imagens
        images = self.convert_pdf_to_images(file)
        
        # 4. Análise por IA
        ai_analysis = self.analyze_document_with_ai(document_type, text_content, images)
        
        # 5. Resultado final
        return {
            "status": "sucesso",
            "validacao_arquivo": file_validation,
            "analise_ia": ai_analysis,
            "texto_extraido": text_content[:500] + "..." if len(text_content) > 500 else text_content,
            "total_paginas": len(images)
        }

def create_document_upload_interface():
    """Interface de upload de documentos no Streamlit"""
    
    st.subheader("📄 Upload de Documentos Portuários")
    
    # Configuração da API OpenAI
    openai_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Necessário para análise por IA")
    
    if not openai_key:
        st.warning("⚠️ Configure sua OpenAI API Key na barra lateral para habilitar a análise por IA")
        return
    
    analyzer = RealDocumentAnalyzer(openai_key)
    
    # Seleção do tipo de documento
    document_types = list(analyzer.porto_santos_rules.keys())
    selected_type = st.selectbox(
        "Tipo de Documento",
        document_types,
        help="Selecione o tipo de documento que será enviado"
    )
    
    # Informações sobre o documento selecionado
    rules = analyzer.porto_santos_rules[selected_type]
    with st.expander(f"ℹ️ Regras para {rules['description']}"):
        st.write(f"**Campos obrigatórios:** {', '.join(rules['required_fields'])}")
        st.write(f"**Formato:** {rules['format']}")
        st.write(f"**Tamanho máximo:** {rules['max_size_mb']}MB")
    
    # Upload do arquivo
    uploaded_file = st.file_uploader(
        f"Enviar {rules['description']}",
        type=['pdf'],
        help=f"Envie um arquivo PDF com no máximo {rules['max_size_mb']}MB"
    )
    
    if uploaded_file:
        # Mostra informações do arquivo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nome", uploaded_file.name)
        with col2:
            st.metric("Tamanho", f"{round(uploaded_file.size/(1024*1024), 2)} MB")
        with col3:
            st.metric("Tipo", uploaded_file.type)
        
        # Botão para processar
        if st.button("🔍 Analisar Documento", type="primary"):
            with st.spinner("Analisando documento..."):
                result = analyzer.process_document(uploaded_file, selected_type)
                
                if result["status"] == "erro":
                    st.error(f"❌ {result['mensagem']}")
                    st.json(result["detalhes"])
                else:
                    # Mostra resultados da análise
                    st.success("✅ Documento processado com sucesso!")
                    
                    # Análise por IA
                    ai_result = result["analise_ia"]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if ai_result["valido"]:
                            st.success("✅ Documento Válido")
                        else:
                            st.error("❌ Documento Inválido")
                    
                    with col2:
                        st.metric("Score de Conformidade", f"{ai_result['score_conformidade']}/100")
                    
                    # Campos encontrados/faltantes
                    if ai_result["campos_encontrados"]:
                        st.write("**✅ Campos Encontrados:**")
                        for campo in ai_result["campos_encontrados"]:
                            st.write(f"- {campo}")
                    
                    if ai_result["campos_faltantes"]:
                        st.write("**❌ Campos Faltantes:**")
                        for campo in ai_result["campos_faltantes"]:
                            st.write(f"- {campo}")
                    
                    # Observações e recomendações
                    if ai_result["observacoes"]:
                        with st.expander("📝 Observações"):
                            for obs in ai_result["observacoes"]:
                                st.write(f"• {obs}")
                    
                    if ai_result["recomendacoes"]:
                        with st.expander("💡 Recomendações"):
                            for rec in ai_result["recomendacoes"]:
                                st.write(f"• {rec}")
                    
                    # Texto extraído
                    with st.expander("📄 Texto Extraído"):
                        st.text_area("Conteúdo", result["texto_extraido"], height=200)

# Exemplo de uso
if __name__ == "__main__":
    create_document_upload_interface()
