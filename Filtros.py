import streamlit as st
import pandas as pd
import datetime
# Função para carregar os dados
@st.cache_data
def carregar_dados():
    tabela = pd.read_csv("Avel_Dallastra.csv")
    # Converter a coluna 'Data' para datetime64[ns]
    tabela['Data'] = pd.to_datetime(tabela['Data'])
    return tabela

def pagina_filtros():
    st.sidebar.header("Filtros")
    dados = carregar_dados()

    # Filtrar por jogador
    jogadores = st.sidebar.multiselect("Selecione o(s) jogador(es)", dados['Jogador'].unique())
    # Filtrar por ano
    anos = st.sidebar.multiselect("Selecione o(s) ano(s)", sorted(dados['Ano'].unique()))
    # FIltrar por Tipo de Duraçao
    site = st.sidebar.multiselect("Selecione o(s) site(s)", (dados['Site'].unique()))
    # FIltrar por Tipo de Duraçao
    nick = st.sidebar.multiselect("Selecione o(s) nickname(s)", (dados['Nickname'].unique()))
    # Filtrar por Tamanho do Field
    tamanho_field = st.sidebar.multiselect("Selecione o(s) tamanho(s) do field", sorted(dados['Tamanho do Field'].unique()))
    # Filtrar por Intervalo de Buy in
    intervalo_buyin = st.sidebar.multiselect("Selecione o(s) intervalo(s) de buy-in", sorted(dados['Intervalo de Buy in'].unique()))
    # Filtrar por Dia da Semana
    dia_semana = st.sidebar.multiselect("Selecione o(s) dia(s) da semana", sorted(dados['Dia da Semana'].unique()))
    # Filtrar por Mês
    mes = st.sidebar.multiselect("Selecione o(s) mês(es)", sorted(dados['Mês'].unique()))
    # FIltrar por Tipo de Torneio
    tipo_de_torneio = st.sidebar.multiselect("Selecione o(s) tipos de torneio(s)", sorted(dados['Tipo de Torneio'].unique()))
    # FIltrar por Tipo de Duraçao
    tipo_de_duraçao = st.sidebar.multiselect("Selecione o(s) tipos de duraçoes(s)", (dados['Tipo de Duraçao'].unique()))
    # FIltrar por Tipo de Duraçao
    tipo_de_intervalo = st.sidebar.multiselect("Selecione o(s) tipos de intervalo(s) de horário(s)", sorted(dados['Intervalo Horario'].unique()))
    # FIltrar por Tipo de Duraçao
    moeda = st.sidebar.multiselect("Selecione a(s) moeda(s)", (dados['Moeda'].unique()))
    # FIltrar por Tipo de Duraçao
    rebuy = st.sidebar.multiselect("Selecione a quantidade de rebuys)", [int(rebuy) for rebuy in dados['Rebuys'].unique()])
    # FIltrar por Tipo de Duraçao
    velocidade = st.sidebar.multiselect("Selecione a(s) velocidade(s)", (dados['Velocidade'].unique()))

    # Se o nickname existe, continue com a execução normalmente
    return jogadores, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade
