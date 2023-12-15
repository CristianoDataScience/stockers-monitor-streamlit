import yfinance as yf
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
from PIL import Image


def consulta_acao(acao):
    # Obtendo os dados da ação
    dados_acao = yf.Ticker(acao)
    historico = dados_acao.history(period="1mo")
    return historico


def main():
    st.title('Consulta de Ações')

    # Adicionando a imagem acima do seletor de ações na barra lateral
    imagem = Image.open('logo.jpeg')
    st.sidebar.image(imagem, caption='Imagem de referência')

    acoes = ['CIEL3.SA', 'PETR4.SA', 'USIM5.SA']
    fundos_imobiliarios = ['MXRF11.SA', 'GALG11.SA']
    opcao = st.sidebar.selectbox('Selecione o ativo para consultar', acoes + fundos_imobiliarios)

    st.subheader(f'Dados para {opcao}')

    if opcao in acoes:
        # Exibir dados para ações
        dados = consulta_acao(opcao)
        st.write(dados.tail(30))  # 252 dias úteis em 12 meses
        # Plotar gráfico de velas para ações
        fig = make_subplots(rows=1, cols=1)
        candlestick = go.Candlestick(x=dados.index,
                                     open=dados['Open'],
                                     high=dados['High'],
                                     low=dados['Low'],
                                     close=dados['Close'])

        fig.add_trace(candlestick)
        fig.update_layout(title=f'Gráfico de Vela para {opcao}',
                          xaxis_title='Data',
                          yaxis_title='Preço',
                          template='plotly_dark')

        st.plotly_chart(fig)
    else:
        # Exibir dados para fundos imobiliários
        dados_fundos = consulta_acao(opcao)
        st.write(dados_fundos.tail(30))  # 90 dias úteis em 12 meses
        # Plotar gráfico de linha para fundos imobiliários
        fig_fundos = go.Figure()
        fig_fundos.add_trace(go.Scatter(x=dados_fundos.index, y=dados_fundos['Close'], mode='lines', name='Fechamento'))
        fig_fundos.update_layout(title=f'Gráfico de Fechamento para {opcao}',
                                 xaxis_title='Data',
                                 yaxis_title='Preço',
                                 template='plotly_dark')

        st.plotly_chart(fig_fundos)


if __name__ == '__main__':
    main()
