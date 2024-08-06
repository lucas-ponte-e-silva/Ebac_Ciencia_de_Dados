#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import streamlit as st
import numpy as np

sns.set_theme()  

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    fig, ax = plt.subplots(figsize=(15, 5))
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).plot(ax=ax)
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).sort_values(value).plot(ax=ax)
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).unstack().plot(ax=ax)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    st.pyplot(fig)

st.set_page_config(page_title = "SINASC Rondônia",
                   page_icon = "https://upload.wikimedia.org/wikipedia/commons/b/b3/Bras%C3%A3o_de_Rond%C3%B4nia.png",
                   layout = "wide")

st.title('Análise SINASC')

st.warning('This is a warning', icon="⚠️")

# Adicionando o uploader de arquivos
uploaded_files = st.file_uploader("Escolha os arquivos CSV do SINASC", accept_multiple_files=True)

if uploaded_files:
    # Se arquivos foram carregados, use-os
    sinasc = pd.concat([pd.read_csv(file) for file in uploaded_files])
else:
    # Se nenhum arquivo foi carregado, use os arquivos locais
    input_path = r"C:\Users\ottop\OneDrive\Área de Trabalho\Curso Ciencia de Dados Ebac\Ebac_Ciencia_de_Dados\Desenvolvimento de aplicações com Python - 05\Scripting - 06\input"
    meses = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN']
    sinasc = pd.concat([pd.read_csv(os.path.join(input_path, f'SINASC_RO_2019_{mes}.csv')) for mes in meses])

st.success('This is a success message!', icon="✅")

sinasc.DTNASC = pd.to_datetime(sinasc.DTNASC)

st.write(f"Data mínima: {sinasc.DTNASC.min()}")
st.write(f"Data máxima: {sinasc.DTNASC.max()}")

data_inicial, data_final = st.sidebar.date_input('Periodo de Intervalo',
                                                 value=[sinasc.DTNASC.min().date(), sinasc.DTNASC.max().date()],
                                                 min_value=sinasc.DTNASC.min().date(),
                                                 max_value=sinasc.DTNASC.max().date())

# Filtrar o DataFrame com base no intervalo de datas selecionado
sinasc_filtrado = sinasc[(sinasc.DTNASC.dt.date >= data_inicial) & (sinasc.DTNASC.dt.date <= data_final)]

st.balloons()

st.dataframe(sinasc_filtrado)

sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
selected = st.feedback("thumbs")
if selected is not None:
    st.markdown(f"You selected: {sentiment_mapping[selected]}")

# Gerar os gráficos
st.divider()
st.subheader("Quantidade de Nascimentos por Data")
plota_pivot_table(sinasc_filtrado, 'IDADEMAE', 'DTNASC', 'count', 'quantidade de nascimento', 'data de nascimento')
st.divider()
st.subheader("Média de Idade da Mãe por Data e Sexo do Bebê")
plota_pivot_table(sinasc_filtrado, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae', 'data de nascimento', 'unstack')
st.divider()
st.subheader("Média de Peso do Bebê por Data e Sexo")
plota_pivot_table(sinasc_filtrado, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe', 'data de nascimento', 'unstack')
st.divider()
st.subheader("APGAR1 Médio por Escolaridade da Mãe")
plota_pivot_table(sinasc_filtrado, 'PESO', 'ESCMAE', 'median', 'apgar1 medio', 'gestacao', 'sort')
st.divider()
st.subheader("APGAR1 Médio por Tempo de Gestação")
plota_pivot_table(sinasc_filtrado, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio', 'gestacao', 'sort')
st.divider()
st.subheader("APGAR5 Médio por Tempo de Gestação")
plota_pivot_table(sinasc_filtrado, 'APGAR5', 'GESTACAO', 'mean', 'apgar5 medio', 'gestacao', 'sort')
    


# In[ ]:




