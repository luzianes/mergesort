import random
import numpy as np
import matplotlib.pyplot as plt

def gerar_entrada_aleatoria(tamanho, limite_inferior=0, limite_superior=1000):
    """
    Gera uma lista de números inteiros aleatórios.
    
    :param tamanho: Número de elementos na lista
    :param limite_inferior: Menor valor possível
    :param limite_superior: Maior valor possível
    :return: Lista de números aleatórios
    """
    return [random.randint(limite_inferior, limite_superior) for _ in range(tamanho)]

def gerar_entrada_ordenada(tamanho, ordem='crescente'):
    """
    Gera uma lista ordenada (crescente ou decrescente).
    
    :param tamanho: Número de elementos na lista
    :param ordem: 'crescente' ou 'decrescente'
    :return: Lista ordenada
    """
    lista = list(range(tamanho))
    return lista if ordem == 'crescente' else list(reversed(lista))

def gerar_entrada_quase_ordenada(tamanho, percentual_desordem=10):
    """
    Gera uma lista quase ordenada com uma porcentagem de elementos fora de ordem.
    
    :param tamanho: Número de elementos na lista
    :param percentual_desordem: Porcentagem de elementos que serão embaralhados
    :return: Lista quase ordenada
    """
    lista = list(range(tamanho))
    num_desordenados = int(tamanho * percentual_desordem / 100)
    
    # Embaralha uma porção dos elementos
    indices_desordenados = random.sample(range(tamanho), num_desordenados)
    valores_desordenados = [lista[i] for i in indices_desordenados]
    random.shuffle(valores_desordenados)
    
    for i, indice in enumerate(indices_desordenados):
        lista[indice] = valores_desordenados[i]
    
    return lista

def gerar_entrada_com_duplicatas(tamanho, num_duplicatas=3):
    """
    Gera uma lista com duplicatas.
    
    :param tamanho: Número de elementos na lista
    :param num_duplicatas: Número de valores que serão repetidos
    :return: Lista com duplicatas
    """
    lista = list(range(tamanho - num_duplicatas))
    duplicatas = [random.choice(lista) for _ in range(num_duplicatas)]
    lista.extend(duplicatas)
    random.shuffle(lista)
    return lista

def salvar_entrada(lista, nome_arquivo):
    """
    Salva a lista em um arquivo de texto.
    
    :param lista: Lista a ser salva
    :param nome_arquivo: Nome do arquivo de saída
    """
    with open(nome_arquivo, 'w') as f:
        f.write('\n'.join(map(str, lista)))

def visualizar_distribuicao(lista, titulo='Distribuição dos Dados'):
    """
    Cria um histograma da distribuição dos dados.
    
    :param lista: Lista de números
    :param titulo: Título do gráfico
    """
    plt.figure(figsize=(10, 6))
    plt.hist(lista, bins='auto', edgecolor='black')
    plt.title(titulo)
    plt.xlabel('Valor')
    plt.ylabel('Frequência')
    plt.tight_layout()
    plt.savefig(f'{titulo.replace(" ", "_")}.png')
    plt.close()

def main():
    # Tamanhos de entrada para teste
    tamanhos = [100, 1000, 10000]
    
    # Gera diferentes tipos de entradas
    tipos_entradas = [
        ('aleatoria', gerar_entrada_aleatoria),
        ('ordenada_crescente', lambda t: gerar_entrada_ordenada(t, 'crescente')),
        ('ordenada_decrescente', lambda t: gerar_entrada_ordenada(t, 'decrescente')),
        ('quase_ordenada', gerar_entrada_quase_ordenada),
        ('com_duplicatas', gerar_entrada_com_duplicatas)
    ]
    
    # Gera e salva entradas
    for tamanho in tamanhos:
        for nome, gerador in tipos_entradas:
            # Gera entrada
            entrada = gerador(tamanho)
            
            # Salva entrada em arquivo
            nome_arquivo = f'entrada_{nome}_{tamanho}.txt'
            salvar_entrada(entrada, nome_arquivo)
            
            # Visualiza distribuição
            visualizar_distribuicao(entrada, f'Distribuição {nome} {tamanho}')
            
            print(f'Gerado: {nome_arquivo}')

if __name__ == '__main__':
    main()