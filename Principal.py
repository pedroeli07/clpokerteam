import streamlit as st
from Filtros import pagina_filtros, carregar_dados
import pandas as pd
import plotly.express as px
import datetime

# Função para criar e atualizar os gráficos
def criar_grafico(jogadores, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, tipo_grafico, dados):    
    # Filtrar os dados com base nos filtros selecionados
    dados_filtrados = dados.copy()

    if jogadores:
        dados_filtrados = dados_filtrados[dados_filtrados['Jogador'].isin(jogadores)]
    if anos:
        dados_filtrados = dados_filtrados[dados_filtrados['Ano'].isin(anos)]
    if site:
        dados_filtrados = dados_filtrados[dados_filtrados['Site'].isin(site)]
    if nick:
        dados_filtrados = dados_filtrados[dados_filtrados['Nickname'].isin(nick)]
    if tamanho_field:
        dados_filtrados = dados_filtrados[dados_filtrados['Tamanho do Field'].isin(tamanho_field)]
    if intervalo_buyin:
        dados_filtrados = dados_filtrados[dados_filtrados['Intervalo de Buy in'].isin(intervalo_buyin)]
    if dia_semana:
        dados_filtrados = dados_filtrados[dados_filtrados['Dia da Semana'].isin(dia_semana)]
    if mes:
        dados_filtrados = dados_filtrados[dados_filtrados['Mês'].isin(mes)]
    if tipo_de_torneio:
        dados_filtrados = dados_filtrados[dados_filtrados['Tipo de Torneio'].isin(tipo_de_torneio)]
    if tipo_de_duraçao:
        dados_filtrados = dados_filtrados[dados_filtrados['Tipo de Duraçao'].isin(tipo_de_duraçao)]
    if tipo_de_intervalo:
        dados_filtrados = dados_filtrados[dados_filtrados['Intervalo Horario'].isin(tipo_de_intervalo)]
    if moeda:
        dados_filtrados = dados_filtrados[dados_filtrados['Moeda'].isin(moeda)]
    if rebuy:
        dados_filtrados = dados_filtrados[dados_filtrados['Rebuys'].isin(rebuy)]
    if velocidade:
        dados_filtrados = dados_filtrados[dados_filtrados['Velocidade'].isin(velocidade)]

    # Verificar se há dados para exibir
    if dados_filtrados.empty:
        st.warning("Não há dados disponíveis para os filtros selecionados.")
        return

    # Calcula o lucro acumulado por ano e jogador
    lucro_por_ano_jogador = dados_filtrados.groupby(['Ano', 'Jogador'])['Profit USD'].sum().reset_index()

    # Plotar o gráfico selecionado
    fig = None
    if tipo_grafico == "Gráfico de Linhas":
        # Recalcula o valor acumulado
        dados_filtrados = dados_filtrados.sort_values(by='Data')  # Ordenar os dados pela coluna 'Data'
        dados_filtrados['Profit USD Acumulado'] = dados_filtrados.groupby('Jogador')['Profit USD'].cumsum()  # Calcular o valor acumulado por jogador
        fig = px.line(dados_filtrados, x='Data', y='Profit USD Acumulado', color='Jogador', title='Lucro acumulado ao longo do tempo')
    elif tipo_grafico == "Gráfico de Barras":
        fig = px.bar(lucro_por_ano_jogador, x='Ano', y='Profit USD', color='Jogador', barmode='group', title='Lucro acumulado por ano')
    elif tipo_grafico == "Gráfico de Pizza":
        # Filtrar os dados por jogador
        for jogador_selecionado in jogadores:
            dados_jogador = lucro_por_ano_jogador[lucro_por_ano_jogador['Jogador'] == jogador_selecionado]
            fig_jogador = px.pie(dados_jogador, values='Profit USD', names='Ano', title=f'Lucro acumulado por ano para {jogador_selecionado}')
            st.plotly_chart(fig_jogador)
    elif tipo_grafico == "Gráfico de Dispersão":
        dados_filtrados = dados_filtrados.sort_values(by='Data')
        dados_filtrados['Profit USD Acumulado'] = dados_filtrados.groupby('Jogador')['Profit USD'].cumsum()
        fig = px.scatter(dados_filtrados, x='Data', y='Profit USD Acumulado', color='Jogador', title='Gráfico de Dispersão')
    elif tipo_grafico == "Gráfico de Área":
        dados_filtrados = dados_filtrados.sort_values(by='Data')
        dados_filtrados['Profit USD Acumulado'] = dados_filtrados.groupby('Jogador')['Profit USD'].cumsum()
        fig = px.area(dados_filtrados, x='Data', y='Profit USD Acumulado', color='Jogador', title='Gráfico de Área')


    # Exibir o gráfico
    if fig is not None:
        st.plotly_chart(fig)


# Adicionar logo do CL Poker Team no alto da barra lateral
st.sidebar.image("logo.jpg", use_column_width=True)

# Definir título do seletor de página
st.sidebar.title("Navegação")

# Verificar qual página deve ser exibida
opcao_pagina = st.sidebar.radio("Selecione a página:", options=["Home", "Filtros"])

# Exibir a página selecionada
if opcao_pagina == "Home":
    st.header("Análise de torneios dos jogadores do CL Poker Team")
    st.subheader("Dashboard de Avelange Jr e Dallastra")
    st.write("Informações sobre os jogadores coletadas do Sharkscope")
    st.write("Fonte dos dados : [Sharkscope](https://www.sharkscope.com/)")
    st.write("Desenvolvido por Pedro Eli Bernardes Maciel")

    # Link do WhatsApp com emoji e imagem
    st.markdown("[Mensagem no WhatsApp](https://wa.me/5537998734398) <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/1200px-WhatsApp.svg.png' alt='WhatsApp' width='20'>", unsafe_allow_html=True)

    # Link do LinkedIn com emoji e imagem
    st.markdown("[Perfil no LinkedIn](https://www.linkedin.com/in/pedro-eli-bernardes-maciel-904828296/) <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Linkedin_icon.svg/1200px-Linkedin_icon.svg.png' alt='LinkedIn' width='20'>", unsafe_allow_html=True)


elif opcao_pagina == "Filtros":
    jogadores, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade = pagina_filtros()
    dados = carregar_dados()


    # Definir todas as combinações possíveis de gráficos
    opcoes_graficos = {
        "Gráfico de Linhas": ("Gráfico de Linhas",),
        "Gráfico de Barras": ("Gráfico de Barras",),
        "Gráfico de Pizza": ("Gráfico de Pizza",),
        "Gráfico de Dispersão": ("Gráfico de Dispersão",),
        "Gráfico de Área": ("Gráfico de Área",),
        "Gráfico de Linhas e Barras": ("Gráfico de Linhas", "Gráfico de Barras"),
        "Gráfico de Linhas e Pizza": ("Gráfico de Linhas", "Gráfico de Pizza"),
        "Gráfico de Linhas e Dispersão": ("Gráfico de Linhas", "Gráfico de Dispersão"),
        "Gráfico de Linhas e Área": ("Gráfico de Linhas", "Gráfico de Área"),
        "Gráfico de Barras e Pizza": ("Gráfico de Barras", "Gráfico de Pizza"),
        "Gráfico de Barras e Dispersão": ("Gráfico de Barras", "Gráfico de Dispersão"),
        "Gráfico de Barras e Área": ("Gráfico de Barras", "Gráfico de Área"),
        "Gráfico de Pizza e Dispersão": ("Gráfico de Pizza", "Gráfico de Dispersão"),
        "Gráfico de Pizza e Área": ("Gráfico de Pizza", "Gráfico de Área"),
        "Gráfico de Dispersão e Área": ("Gráfico de Dispersão", "Gráfico de Área"),
        "Gráfico de Linhas, Barras e Pizza": ("Gráfico de Linhas", "Gráfico de Barras", "Gráfico de Pizza"),
        "Gráfico de Linhas, Barras e Dispersão": ("Gráfico de Linhas", "Gráfico de Barras", "Gráfico de Dispersão"),
        "Gráfico de Linhas, Barras e Área": ("Gráfico de Linhas", "Gráfico de Barras", "Gráfico de Área"),
        "Gráfico de Linhas, Pizza e Dispersão": ("Gráfico de Linhas", "Gráfico de Pizza", "Gráfico de Dispersão"),
        "Gráfico de Linhas, Pizza e Área": ("Gráfico de Linhas", "Gráfico de Pizza", "Gráfico de Área"),
        "Gráfico de Linhas, Dispersão e Área": ("Gráfico de Linhas", "Gráfico de Dispersão", "Gráfico de Área"),
        "Gráfico de Barras, Pizza e Dispersão": ("Gráfico de Barras", "Gráfico de Pizza", "Gráfico de Dispersão"),
        "Gráfico de Barras, Pizza e Área": ("Gráfico de Barras", "Gráfico de Pizza", "Gráfico de Área"),
        "Gráfico de Barras, Dispersão e Área": ("Gráfico de Barras", "Gráfico de Dispersão", "Gráfico de Área"),
        "Gráfico de Pizza, Dispersão e Área": ("Gráfico de Pizza", "Gráfico de Dispersão", "Gráfico de Área"),
        "Gráfico de Linhas, Barras, Pizza e Dispersão": ("Gráfico de Linhas", "Gráfico de Barras", "Gráfico de Pizza", "Gráfico de Dispersão"),
        "Gráfico de Linhas, Barras, Pizza e Área": ("Gráfico de Linhas", "Gráfico de Barras", "Gráfico de Pizza", "Gráfico de Área"),
        "Gráfico de Linhas, Barras, Dispersão e Área": ("Gráfico de Linhas", "Gráfico de Barras", "Gráfico de Dispersão", "Gráfico de Área"),
        "Gráfico de Linhas, Pizza, Dispersão e Área": ("Gráfico de Linhas", "Gráfico de Pizza", "Gráfico de Dispersão", "Gráfico de Área"),
        "Gráfico de Barras, Pizza, Dispersão e Área": ("Gráfico de Barras", "Gráfico de Pizza", "Gráfico de Dispersão", "Gráfico de Área"),
        "Todos os Gráficos": (
            "Gráfico de Linhas", "Gráfico de Barras", "Gráfico de Pizza", "Gráfico de Dispersão", "Gráfico de Área",
            "Gráfico de Linhas e Barras", "Gráfico de Linhas e Pizza", "Gráfico de Linhas e Dispersão", "Gráfico de Linhas e Área",
            "Gráfico de Barras e Pizza", "Gráfico de Barras e Dispersão", "Gráfico de Barras e Área",
            "Gráfico de Pizza e Dispersão", "Gráfico de Pizza e Área",
            "Gráfico de Dispersão e Área",
            "Gráfico de Linhas, Barras e Pizza", "Gráfico de Linhas, Barras e Dispersão", "Gráfico de Linhas, Barras e Área",
            "Gráfico de Linhas, Pizza e Dispersão", "Gráfico de Linhas, Pizza e Área",
            "Gráfico de Linhas, Dispersão e Área",
            "Gráfico de Barras, Pizza e Dispersão", "Gráfico de Barras, Pizza e Área",
            "Gráfico de Barras, Dispersão e Área",
            "Gráfico de Pizza, Dispersão e Área",
            "Gráfico de Linhas, Barras, Pizza e Dispersão",
            "Gráfico de Linhas, Barras, Pizza e Área",
            "Gráfico de Linhas, Barras, Dispersão e Área",
            "Gráfico de Linhas, Pizza, Dispersão e Área",
            "Gráfico de Barras, Pizza, Dispersão e Área",
        )
    }
    # Opções de gráficos
    opcao_grafico = st.selectbox("Selecione o tipo de gráfico:", opcoes_graficos)


    # Verificar se a opção selecionada está no dicionário e chamar a função correspondente
    if opcao_grafico in opcoes_graficos:
        graficos = opcoes_graficos[opcao_grafico]
        for grafico in graficos:
            criar_grafico(jogadores, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, grafico, dados)
    else:
        st.error("Opção de gráfico inválida.")


        