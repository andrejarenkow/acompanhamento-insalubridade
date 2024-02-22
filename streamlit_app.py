from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import streamlit as st
from datetime import datetime
import pytz

# Configurações da página
st.set_page_config(
    page_title="Insalubridade",
    page_icon="	:100:",
    layout="wide",
    initial_sidebar_state='collapsed'
) 

#definição da função
def obter_dados(numero_proa):

#obtenção do link de consulta do proa
  link_proa = 'https://secweb.procergs.com.br/pra-aj4/public/proa_retorno_consulta_publica.xhtml?numeroProcesso='+numero_proa
  response = urlopen(link_proa)
  html = response.read()
  soup = BeautifulSoup(html, 'html.parser')

#criação da lista com as informações que voltam após o scraping
  infos = []
  for i in soup.find_all('td'):
    infos.append(i.get_text().strip())

#os números pares são os setores, requerente, etc, ou seja, o nome das colunas
  cabecalhos = [0,2,4,6,8,10,12,14,16,18]

#os ímpares são os valores correspondentes
  respostas = [1,3,5,7,9,11,13,15,17,19]
  lista = {}
  for i,j in zip(cabecalhos, respostas):
    lista[infos[i]] = infos[j]

  return lista


processos = ['24200000150626','24200000143158','24200000059505',
             '24200000150600','24200000150650','24200000021508',
             '24200000151193','24200000053795','24200000078534']

today = datetime.now(pytz.timezone('America/Sao_Paulo'))

resposta_processos = []
for i in processos:
  print(i)
  resposta_processos.append(obter_dados(i))

dados = pd.DataFrame(resposta_processos)
dados['data_da_consulta'] = str(today)


datas = ['Data de Abertura:','Data Atividade atual (data de recebimento):','Data de Aquisição Atividade atual:', 'data_da_consulta']
for i in datas:
  dados[i] = pd.to_datetime(dados[i], dayfirst=True)


dados.sort_values('Data Atividade atual (data de recebimento):', ascending=False, inplace=True)#.to_excel('dados_insalubridade_2023-03-20.xlsx', index=False)

for i in datas:
  dados[i] = dados[i].astype(str)
  dados[i] = dados[i].str.replace('NaT','Não adquirido')


dados
