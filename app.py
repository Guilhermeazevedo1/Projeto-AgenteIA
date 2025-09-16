import os
import streamlit as st
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

st.title("Professor Java")

# Seleção do modelo
model = st.selectbox(
    " Escolha o modelo:",
    ["deepseek-r1-distill-llama-70b"]
)

# Entrada do prompt
prompt = st.text_area(" Digite sua pergunta:")

if st.button("Gerar resposta"):

        try:
            
            api_key = os.getenv("GROQ_API_KEY")
            
            # Inicializa o modelo
            llm = ChatGroq(
                groq_api_key= api_key,
                model_name= "deepseek-r1-distill-llama-70b"
            )

            # Template de prompt
            template = ChatPromptTemplate.from_messages([
                ("system", "Você é Professor de programação."),
                ("human", "{prompt}")
            ])

            chain = template | llm

            # Executa a cadeia
            with st.spinner("Gerando resposta..."):
                res = chain.invoke({"prompt": prompt})
                resposta = res.content
                resposta = re.sub(r"<think>.*?</think>", "", resposta, flags=re.DOTALL)
                st.success("Resposta gerada com sucesso!")
                st.write("### 💬 Resposta:")
                st.write(resposta.strip())

        except Exception as e:
            st.error(f"Erro: {e}")