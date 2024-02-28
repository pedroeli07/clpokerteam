
import pandas as pd
import plotly.express as px
import datetime
import streamlit as st
from Filtros import pagina_filtros, carregar_dados
from Graficos import criar_grafico
import plotly.graph_objects as go
import streamlit.components.v1 as components
from Graficos_filtro import criar_grafico_filtros
# Configura a largura da página para ocupar toda a tela
st.set_page_config(layout="wide")
# Adicionar logo do CL Poker Team no alto da barra lateral
st.sidebar.image("logo.jpg", use_column_width=True)

# Definir título do seletor de página
st.sidebar.title("Navegação")

# Verificar qual página deve ser exibida
opcao_pagina = st.sidebar.radio("Selecione a página:", options=["Home", "Filtros"])

# Exibir a página selecionada
if opcao_pagina == "Home":
    # Adicionando emojis
    emoji_espadas = "♠️"
    emoji_copas = "♥️"
    emoji_ouros = "♦️"
    emoji_paus = "♣️"
    emoji_trofeu = "🏆"
    emoji_grafico = "📈"
    # Títulos com emojis
    st.header(f"{emoji_espadas}{emoji_copas}{emoji_ouros}{emoji_paus}{emoji_trofeu} Analisando jogadores do CL Team Poker {emoji_espadas}{emoji_copas}{emoji_ouros}{emoji_paus}{emoji_trofeu}")
    st.subheader(f"{emoji_grafico} Dashboard de Avelange Jr e Dallastra {emoji_grafico}")
    st.write("Informações sobre os jogadores coletadas do Sharkscope")
    st.write("Fonte dos dados : [Sharkscope](https://www.sharkscope.com/)")
    st.write("Desenvolvido por Pedro Eli Bernardes Maciel")

    # Link do WhatsApp com emoji e imagem
    st.markdown("[Mensagem no WhatsApp](https://wa.me/5537998734398) <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/1200px-WhatsApp.svg.png' alt='WhatsApp' width='20'>", unsafe_allow_html=True)

    # Link do LinkedIn com emoji e imagem
    st.markdown("[Perfil no LinkedIn](https://www.linkedin.com/in/pedro-eli-bernardes-maciel-904828296/) <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Linkedin_icon.svg/1200px-Linkedin_icon.svg.png' alt='LinkedIn' width='20'>", unsafe_allow_html=True)

elif opcao_pagina == "Filtros":
    anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade = pagina_filtros()
    dados = carregar_dados()

    # Definir todas as combinações possíveis de gráficos
    opcoes_graficos = {
        "Gráfico de Linhas": False,
        "Gráfico de Barras": False,
        "Gráfico de Pizza": False,
        "Gráfico de Dispersão": False,
        "Gráfico de Área": False,
    }
       # Dividir a tela em duas colunas
    col3, col4 = st.columns([1, 1])
    with col3:
        st.sidebar.header("Filtros")
        dados = carregar_dados()

        # Texto para instruir o usuário
        st.header("Selecione o(s) jogador(es):")
        
        # Lista para armazenar os jogadores selecionados
        jogadores = []
        # Número de colunas desejadas para os jogadores
        num_colunas = 4
        # Obter o número total de jogadores
        num_jogadores = len(dados['Jogador'].unique())
        # Calcular o número total de linhas necessárias
        num_linhas = -(-num_jogadores // num_colunas)  # Arredondamento para cima da divisão
        # Largura desejada para as imagens dos jogadores (em pixels)
        largura_imagem = 100
        # Exibir checkbox para cada jogador em um layout de várias colunas
        for linha in range(num_linhas):
            # Criar uma nova linha para os jogadores
            colunas_jogadores = st.columns(num_colunas)
            # Iterar sobre as colunas para exibir os jogadores
            for coluna in range(num_colunas):
                # Calcular o índice do jogador na lista de jogadores
                jogador_index = linha * num_colunas + coluna
                # Verificar se ainda há jogadores a serem exibidos
                if jogador_index < num_jogadores:
                    jogador = dados['Jogador'].unique()[jogador_index]
                    # Carregar a imagem do jogador
                    imagem_jogador = f'{jogador}.jpg'  # Exemplo: 'Avelange Jr.jpg' ou 'Dallastra.jpg'
                    # Exibir a imagem do jogador e o checkbox lado a lado
                    with colunas_jogadores[coluna]:
                        st.image(imagem_jogador, width=largura_imagem)  # Largura da imagem
                        if st.checkbox(jogador):
                            jogadores.append(jogador)

    # Adicionar checkbox para cada tipo de gráfico
    with col4:
        st.header("Opções de Gráficos Individuais")
        for grafico in opcoes_graficos:
            opcoes_graficos[grafico] = st.checkbox(grafico, False)

        # Adicionar checkbox para selecionar todos os tipos de gráficos
        todos_os_graficos = st.checkbox("Todos os Gráficos", False)

    # Se "Todos os Gráficos" estiver selecionado, marcar todas as opções de gráficos
    if todos_os_graficos:
        for grafico in opcoes_graficos:
            opcoes_graficos[grafico] = True

        # Exibir os gráficos selecionados
    for grafico, selecionado in opcoes_graficos.items():
        if selecionado:
            criar_grafico(jogadores, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, grafico, dados)

    # Definir todas as combinações possíveis de gráficos
    opcoes_graficos2 = {
        "Gráfico de Linhas": False,
        "Gráfico de Barras": False,
        "Gráfico de Pizza": False,
        "Gráfico de Dispersão": False,
        "Gráfico de Área": False,
        "Todos os Gráficos": False  # Opção adicional para ver todos os gráficos ao mesmo tempo    
    }
    # Dividir a tela em duas colunas
    col1, col2 = st.columns([1, 1])

    # Adicionar o radio para selecionar o tipo de gráfico na primeira coluna
    with col2:
        st.header("Opções de Gráficos por Filtro")
        opcao_selecionada = st.radio("Selecione o tipo de gráfico", list(opcoes_graficos2.keys()))

    # Adicionar a seleção de jogadores na segunda coluna
    with col1:
        st.header("Selecione o(s) jogador(es):")
        jogadores_selecionados = st.multiselect("Selecione o(s) jogador(es)", list(dados['Jogador'].unique()))


        # Verificar se "Todos os Gráficos" foi selecionado
    if opcao_selecionada == "Todos os Gráficos":
        # Exibir todos os gráficos selecionados para os jogadores escolhidos
        for jogador in jogadores_selecionados:
            for grafico, _ in opcoes_graficos2.items():
                criar_grafico_filtros([jogador], anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, grafico, dados)
    else:
        # Exibir o gráfico selecionado individualmente para os jogadores escolhidos
        for jogador in jogadores_selecionados:
            criar_grafico_filtros([jogador], anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, opcao_selecionada, dados)
        

    def exibir_metricas(jogadores, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, dados):
        # Filtrar os dados com base nos filtros selecionados
        dados_filtrados = dados.copy()

        filtros = {
            'Jogador': jogadores,
            'Ano': anos,
            'Site': site,
            'Nickname': nick,
            'Tamanho do Field': tamanho_field,
            'Intervalo de Buy in': intervalo_buyin,
            'Dia da Semana': dia_semana,
            'Mês': mes,
            'Tipo de Torneio': tipo_de_torneio,
            'Tipo de Duraçao': tipo_de_duraçao,
            'Intervalo Horario': tipo_de_intervalo,
            'Moeda': moeda,
            'Rebuys': rebuy,
            'Velocidade': velocidade
        }

        for coluna, valores in filtros.items():
            if valores:
                dados_filtrados = dados_filtrados[dados_filtrados[coluna].isin(valores)]

        # Calcular a soma das métricas para cada jogador
        metricas_sum = dados_filtrados.groupby('Jogador').agg({
            'Prize USD': 'sum',
            'Rake USD': 'sum',
            'Stake USD': 'sum',
            'Buy-in USD': 'sum',
            'Profit USD': 'sum'
        })

         # Calcular o lucro médio (Profit USD Médio) para cada jogador
        lucro_medio_por_jogador = dados_filtrados.groupby('Jogador')['Profit USD'].mean()
        # Contar o número de torneios para cada jogador
        num_torneios_por_jogador = dados_filtrados.groupby('Jogador').size()
        # Calcular o valor médio de Buy-in USD para cada jogador
        buy_in_usd_medio_por_jogador = metricas_sum['Buy-in USD'] / num_torneios_por_jogador

        # Adicionar a coluna de valor médio de Buy-in USD ao DataFrame
        metricas_sum['Buy in USD Médio'] = buy_in_usd_medio_por_jogador
        # Adicionar as colunas de lucro médio e número de torneios ao DataFrame
        metricas_sum['Profit USD Médio'] = lucro_medio_por_jogador
        metricas_sum['Torneios'] = num_torneios_por_jogador
        # Exibir os totais como DataFrame ocupando toda a largura da tela
        st.write(metricas_sum, use_container_width=True)

    # Outros filtros também podem ser definidos aqui...
    dados = carregar_dados()  # Carregar os dados
    st.header("Métricas:")
    exibir_metricas(jogadores, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, dados)







