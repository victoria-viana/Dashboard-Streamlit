import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 

#Carregando o dado#
hapvida=pd.read_csv('RECLAMEAQUI_HAPVIDA.csv',sep=',')
ibyte=pd.read_csv('RECLAMEAQUI_IBYTE.csv',sep=',')
nagem=pd.read_csv('RECLAMEAQUI_NAGEM.csv',sep=',')

#Incluindo uma coluna para saber de qual empresa se refere o dado#
ibyte['EMPRESA'] = 'IBYTE'
nagem['EMPRESA'] = 'NAGEM'
hapvida['EMPRESA'] = 'HAPVIDA'

#Unindo os dados #
df = pd.concat([ibyte, nagem, hapvida])

#Datetime#
df['TEMPO']=pd.to_datetime(df['TEMPO'])

#Criando a coluna estado#
estado_lista=[]
for i in range(len(df)):
    estado_lista.append(df['LOCAL'].iloc[i].split(' - ',2)[1].strip())
df['ESTADO']=estado_lista

#Limpando o dado#
df['ESTADO'].replace('C', 'CE', inplace=True)
df['ESTADO'].replace('P', 'PB', inplace=True)
df = df[(df['ESTADO'] != '--') & (df['ESTADO'] != 'naoconsta')]


#Streamlit#

st.title('Análise de Sentimento')

st.write('Análise das reclamações no RECLAME AQUI')

lista_empresa=df['EMPRESA'].unique().tolist()
empresa = st.sidebar.selectbox(
    'Selecione a empresa',
    lista_empresa)

lista_estado = df.loc[df['EMPRESA'] == empresa, 'ESTADO'].unique().tolist()
estado = st.sidebar.selectbox(
    'Selecione o estado',
    lista_estado)

lista_status = df.loc[(df['EMPRESA'] == empresa) & (df['ESTADO'] == estado), 'STATUS'].unique().tolist()
status = st.sidebar.selectbox(
    'Selecione o status',
    lista_status)

st.markdown('---')



df_filtrado = df[(df['EMPRESA'] == empresa) & (df['ESTADO'] == estado) & (df['STATUS'] == status)]

fig = px.line(df_filtrado, x='TEMPO', y='CASOS', title=f'Casos para {empresa} no estado de {estado} com status {status}')
st.plotly_chart(fig)


frequencia_estados = df[df['EMPRESA'] == empresa]['ESTADO'].value_counts()

fig2 = px.bar(frequencia_estados, x=frequencia_estados.index, y=frequencia_estados.values,text=frequencia_estados, labels={'x': 'Status', 'y': 'Frequência'}, title=f'Frequência de casos de cada estado da empresa : {empresa} ')
st.plotly_chart(fig2)



frequencia_status = df[df['EMPRESA'] == empresa]['STATUS'].value_counts()

fig2 = px.bar(frequencia_status, x=frequencia_status.index, y=frequencia_status.values,text=frequencia_status, labels={'x': 'Status', 'y': 'Frequência'}, title=f'Frequência de cada caso por status da empresa : {empresa} ')
st.plotly_chart(fig2)


tam_texto= []

for i in range(len(df)):
   tam_texto.append(len(df['DESCRICAO'].iloc[i]))
   
df['TAMANHO_TEXTO'] = tam_texto

frequencia_TAM_TEXT = df[df['EMPRESA'] == empresa]['TAMANHO_TEXTO']

fig5 = px.histogram(frequencia_TAM_TEXT, x='TAMANHO_TEXTO', nbins=100)

st.plotly_chart(fig5)




