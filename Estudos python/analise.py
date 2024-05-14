import os
import time
import json
from random import random
from datetime import datetime
import csv
from sys import argv
import pandas as pd
import seaborn as sns
import requests

URL = 'https://www2.cetip.com.br/ConsultarTaxaDi/ConsultarTaxaDICetip.aspx'

# Loop para extrair dados e salvar no arquivo CSV
for _ in range(0, 10):
    data_e_hora = datetime.now()
    data = datetime.strftime(data_e_hora, '%Y/%m/%d')
    hora = datetime.strftime(data_e_hora, '%H:%M:%S')

    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.HTTPError as exc:
        print("Dado não encontrado, continuando.")
        cdi = None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc
    else:
        dado = json.loads(response.text)
        cdi = float(dado['taxa'].replace(',', '.')) + (random() - 0.5)

    if os.path.exists('./taxa-cdi.csv') == False:
        with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
            fp.write('data,hora,taxa\n')
    
    with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
        fp.write(f'{data},{hora},{cdi}\n')

    time.sleep(2 + (random() - 0.5)) 

print("Extração de dados concluída com sucesso.")

# Leitura dos dados do arquivo CSV e criação do gráfico
df = pd.read_csv('./taxa-cdi.csv')

grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
_ = grafico.set_xticklabels(labels=df['hora'], rotation=90)

nome_do_grafico = argv[1] if len(argv) > 1 else "grafico_taxa_cdi"
grafico.get_figure().savefig(f"{nome_do_grafico}.png")

print(f"Gráfico salvo como {nome_do_grafico}.png")
