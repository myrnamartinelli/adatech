import requests
import json
import functools
from functools import reduce

FILE_PATH = "data/bacen.json"
URL = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='01-01-2023'&@dataFinalCotacao='11-20-2023'&$top=1000&$format=json"

def get_json(url):
    return requests.get(url)

def clean_datahora(data):
    for item in data["value"]:
        item["dataHoraCotacao"] = item["dataHoraCotacao"].split(" ")[0]

    
def save_json(data):
    clean_datahora(data)
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=2)

def get_data():
    """
    Acessa API do Banco Central e retorna os dados referentes à cotação do DOLAR/REAL do ano corrente
    """
    try:
        save_json(get_json(URL).json())
    except Exception as e:
        print("Erro ao obter JSON:", e)

def read_file():
    with open(FILE_PATH) as file:
        return  json.load(file)

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
        

def get_categorias(greater_cotacaoCompra,greater_cotacaoVenda):

    #transforma o dicionário em conjunto
    set_cotacaoCompra = {frozenset(d.items()) for d in greater_cotacaoCompra}
    set_cotacaoVenda = {frozenset(d.items()) for d in greater_cotacaoVenda}
    #acha a intersecção entre os conjuntos
    intersection = set_cotacaoCompra.intersection(set_cotacaoVenda)

    #transforma a intersecção para uma lisra de dicionários
    above_media = [dict(s) for s in intersection]

    return above_media

    

            

    pass

def estatisticas():
    json_file_data = read_file()
    clean_file = clear_data(json_file_data)
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
    above_media = get_categorias(greater_cotacaoCompra,greater_cotacaoVenda)


def main():
    menu_primario()
    
def ordenar_por_datahora(values):
    sorted_values = sorted(values, key=lambda item_da_lista: item_da_lista["dataHoraCotacao"])
    return sorted_values

def add_item(data, datahora, tupla_valor_compra_venda):
    novo_item = {
        "cotacaoCompra": tupla_valor_compra_venda[0],
        "cotacaoVenda": tupla_valor_compra_venda[1],
        "dataHoraCotacao": datahora
    }

    data["value"].append(novo_item)
    data["value"] = ordenar_por_datahora(data["value"])

def edit_item(data, datahora, tupla_valor_compra_venda):
    editado_item = {
        "cotacaoCompra": tupla_valor_compra_venda[0],
        "cotacaoVenda": tupla_valor_compra_venda[1],
        "dataHoraCotacao": datahora
    }

    index_editar = get_datahora_index(data["value"], datahora)

    if index_editar is not None:
        data["value"][index_editar] = editado_item
        data["value"] = ordenar_por_datahora(data["value"])
    else:
        print(f"Data {datahora} não encontrada.")

def get_datahora_index(values, datahora_buscada):
    for index, item in enumerate(values):
        if item["dataHoraCotacao"] == datahora_buscada:
            return index
    return None

def remove_item(data, datahora):
    index_to_remove = get_datahora_index(data["value"], datahora)

    if index_to_remove is not None:
        del data["value"][index_to_remove]
        data["value"] = ordenar_por_datahora(data["value"])
    else:
        print(f"Data {datahora} não encontrada.")

def menu_primario():
    while True:
        print("Escolha o JSON:")
        print("1. Ler arquivo salvo. (offline)")
        print("2. Atualizar arquivo da internet. (online)")
        print("3. Estatísticas.")
        print("4. Sair")
        opcao = input("Escolhe uma opção (1-4): ")
        if opcao == '1':
            menu_secundario()
        elif opcao == '2':
            get_data()
            menu_secundario()
        elif opcao == '3':
            estatisticas()
        elif opcao == '4':
            print("Saindo.")
            break
        else:
            print("Opção inválida. Escolha entre 1 e 4.")

def menu_secundario():
    json_file_data = read_file()

    while True:
        print("Menu:")
        print("1. Adicionar")
        print("2. Editar")
        print("3. Remover")
        print("4. Salvar e voltar")

        opcao = input("Escolha uma opção (1-4): ")

        if opcao == '1':
            datahora = input("Informe a data (YYYY-MM-DD): ")
            valor_compra = float(input("Informe o valor de Compra: "))
            valor_venda = float(input("Informe o valor de Venda: "))
            add_item(json_file_data, datahora, (valor_compra,valor_venda))

        elif opcao == '2':
            datahora = input("Informe a data que deseja modificar (YYYY-MM-DD): ")
            valor_compra = float(input("Informe o NOVO valor de Compra: "))
            valor_venda = float(input("Informe o NOVO valor de Venda: "))
            edit_item(json_file_data, datahora, (valor_compra,valor_venda))

        elif opcao == '3':
            datahora = input("Informe a data que deseja remover (YYYY-MM-DD): ")
            remove_item(json_file_data, datahora)

        elif opcao == '4':
            save_json(json_file_data)
            print("Arquivo JSON atualizado.")
            break

        else:
            print("Opção inválida. Escolha entre 1 e 4.")

    


main()
        

#Permitir que os dados possam ser adicionados, listados, lidos individualmente, atualizados e deletados (manter JSON atualizado) (250XP);

#Garantir que todas as operações tenham validações (try-except, raise) (100XP);

#Obter pelo menos três dados estatístico simples, entre média, mediana, moda e desvio padrão, a partir de algum agrupamento de dados (exemplo, a média de idade do grupo de professores que dão aula de exatas) (utilizar list comprehension) (150XP);

#Salvar dados estatísticos em um CSV (100XP).