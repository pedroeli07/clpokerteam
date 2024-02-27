import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    tabela = pd.read_csv("Avel_Dallastra.csv")
    tabela['Data'] = pd.to_datetime(tabela['Data'])  # Converter a coluna 'Data' para datetime
    return tabela

# Página "Home"
def pagina_home():
    st.header("Análise de torneios dos jogadores do CL Poker Team")
    st.subheader("Dashboard de Avelange Jr e Dallastra")
    st.write("Informações sobre os jogadores coletadas do Sharkscope")
    st.write("Fonte dos dados : [Sharkscope](https://www.sharkscope.com/)")
    st.write("Desenvolvido por Pedro Eli Bernardes Maciel")

    # Link do WhatsApp com emoji e imagem
    st.markdown("[Mensagem no WhatsApp](https://wa.me/5537998734398) <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/1200px-WhatsApp.svg.png' alt='WhatsApp' width='20'>", unsafe_allow_html=True)

    # Link do LinkedIn com emoji e imagem
    st.markdown("[Perfil no LinkedIn](https://www.linkedin.com/in/pedro-eli-bernardes-maciel-904828296/) <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Linkedin_icon.svg/1200px-Linkedin_icon.svg.png' alt='LinkedIn' width='20'>", unsafe_allow_html=True)

# Página "Filtros"
def pagina_filtros():
    st.sidebar.header("Filtros")
    dados = carregar_dados()

    # Filtrar por jogador
    jogadores = st.sidebar.multiselect("Selecione o(s) jogador(es)", dados['Jogador'].unique(), default=["Avelange Jr"])

    # Filtrar por ano
    anos = st.sidebar.multiselect("Selecione o(s) ano(s)", sorted(dados['Ano'].unique()), default=[2021])

    # Filtrar por Tamanho do Field
    tamanho_field = st.sidebar.multiselect("Selecione o(s) tamanho(s) do field", sorted(dados['Tamanho do Field'].unique()))

    # Filtrar por Intervalo de Buy in
    intervalo_buyin = st.sidebar.multiselect("Selecione o(s) intervalo(s) de buy-in", sorted(dados['Intervalo de Buy in'].unique()))

    # Filtrar por Dia da Semana
    dia_semana = st.sidebar.multiselect("Selecione o(s) dia(s) da semana", sorted(dados['Dia da Semana'].unique()))

    # Filtrar por Mês
    mes = st.sidebar.multiselect("Selecione o(s) mês(es)", sorted(dados['Mês'].unique()))

    # Checkbox para selecionar o tipo de gráfico
    tipo_grafico = st.sidebar.radio("Selecione o tipo de gráfico:", options=["Gráfico de Linhas", "Gráfico de Barras", "Gráfico de Pizza"])

    return jogadores, anos, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_grafico
# Função para criar e atualizar os gráficos
def criar_grafico(jogadores, anos, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_grafico):
    dados = carregar_dados()

    # Filtrar os dados pelos jogadores e anos selecionados
    dados_filtrados = dados[dados['Jogador'].isin(jogadores)]

    if anos:
        dados_filtrados = dados_filtrados[dados_filtrados['Ano'].isin(anos)]

    if tamanho_field:
        dados_filtrados = dados_filtrados[dados_filtrados['Tamanho do Field'].isin(tamanho_field)]

    if intervalo_buyin:
        dados_filtrados = dados_filtrados[dados_filtrados['Intervalo de Buy in'].isin(intervalo_buyin)]

    if dia_semana:
        dados_filtrados = dados_filtrados[dados_filtrados['Dia da Semana'].isin(dia_semana)]

    if mes:
        dados_filtrados = dados_filtrados[dados_filtrados['Mês'].isin(mes)]

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
    pagina_home()
elif opcao_pagina == "Filtros":
    jogadores, anos, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_grafico = pagina_filtros()
    criar_grafico(jogadores, anos, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_grafico)