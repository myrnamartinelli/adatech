import requests
import json
import functools
from functools import reduce

FILE_PATH = "data/bacen.json"
URL = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='01-01-2023'&@dataFinalCotacao='11-20-2023'&$top=1000&$format=json"

def get_json(url):
    return requests.get(url)
    
def save_json(response):
    with open(FILE_PATH, "w") as file:
        file.write(response.text)

def get_data():
    """
    Acessa API do Banco Central e retorna os dados referentes à cotação do DOLAR/REAL do ano corrente
    """
    try:
        save_json(get_json(URL))
    except Exception as e:
        print("Erro ao obter JSON:", e)

def read_file():
    with open(FILE_PATH) as file:
        return file.read()
    
def create_dict(json_file):
    """
    Cria um dicionário a partir do arquivo JSON
    """
    data_list = json.loads(json_file)
    return data_list


def clear_data(dict_file):
    """
    Cria uma lista de dicionários onde as chaves são 'cotacaoCompra', 'cotacaoVenda' e 'dataHoraCotacao'
    """
    data_list = []
    for item in dict_file['value']:
        data_list.append(item)

    return data_list
    

def somar_valores_cotacao(clean_file, nome):
    """
    Utiliza o reduce para obter o somatório das cotações
    """
    return reduce(lambda acumulado, elem: acumulado + elem[nome], clean_file, 0 )


def get_media_cotacao(acumulado_cotacao,quantidade):
    media = acumulado_cotacao/quantidade
    return media
    
def get_greater_than(media,tipo_cotacao,clean_file):
    """
    Utiliza filter para criar uma lista que mostra quais cotações estão acima da média
    """
    greater_than = list((filter(lambda elem: elem[tipo_cotacao]>media, clean_file)))
    return greater_than

"""
As próximas 2 funções utiliza o map para gerar listas contendo os valores das diferentes chaves do dicionário. 
Seus retornos são imprescindiveis para o funcionamento da função get_min_max.
"""

def get_dias(clean_file):
    dias_list = list(map(lambda x:x['dataHoraCotacao'], clean_file))
    return dias_list

def get_cotacao_list(clean_file,tipo_cotacao):
    return list(map(lambda x:x[tipo_cotacao],clean_file))
    
    
def get_min_max(nome,tipo_cotacao,ismin = True):

    cotacao_min = tipo_cotacao[0]
    cotacao_max = tipo_cotacao[0]

    for i in range(1,len(tipo_cotacao)):
    
        if tipo_cotacao[i] < cotacao_min:
            cotacao_min = tipo_cotacao[i]

        elif tipo_cotacao[i] > cotacao_max:
            cotacao_max = tipo_cotacao[i]

        min=(nome,cotacao_min)
        max = (nome,cotacao_max)
    if ismin:
        return min
    else:
        return max
        

def get_categorias():
    pass




def main():
    get_data()
    json_file = read_file()
    dict_file = create_dict(json_file)
    clean_file = clear_data(dict_file)
    acumulado_cotacaoCompra = somar_valores_cotacao(clean_file,'cotacaoCompra')
    acumulado_cotacaoVenda = somar_valores_cotacao(clean_file,'cotacaoVenda')
    media_cotacaoCompra = get_media_cotacao(acumulado_cotacaoCompra,len(clean_file))
    media_cotacaoVenda = get_media_cotacao(acumulado_cotacaoVenda,len(clean_file))
    greater_cotacaoCompra = get_greater_than(media_cotacaoCompra,'cotacaoCompra',clean_file)
    greater_cotacaoVenda = get_greater_than(media_cotacaoVenda,'cotacaoVenda',clean_file)
    dias_list = get_dias(clean_file)
    cotacaoCompra_list = get_cotacao_list(clean_file,'cotacaoCompra')
    cotacaoVenda_list = get_cotacao_list(clean_file,'cotacaoVenda')
    tupla_min_max_compra = get_min_max("cotacaoCompra",cotacaoCompra_list, ismin=True)
    tupla_min_max_venda = get_min_max("cotacaoVenda",cotacaoCompra_list)
    print(tupla_min_max_compra)
    print(tupla_min_max_venda)

   

    
   
   


    

    


main()
        

#Permitir que os dados possam ser adicionados, listados, lidos individualmente, atualizados e deletados (manter JSON atualizado) (250XP);

#Garantir que todas as operações tenham validações (try-except, raise) (100XP);

#Esta função deve ter um parâmetro opcional (pode ser de qualquer tipo), que indicará qual das estatísticas você deseja obter (mínimo ou máximo) (150XP);


#Obter pelo menos três dados estatístico simples, entre média, mediana, moda e desvio padrão, a partir de algum agrupamento de dados (exemplo, a média de idade do grupo de professores que dão aula de exatas) (utilizar list comprehension) (150XP);


#Salvar dados estatísticos em um CSV (100XP).