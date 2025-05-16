import random
import numpy as np
import matplotlib.pyplot as plt
import os
import time

def gerar_entrada_aleatoria(tamanho, limite_inferior=0, limite_superior=1000000):
    """
    Gera uma lista de números inteiros aleatórios.
    
    :param tamanho: Número de elementos na lista
    :param limite_inferior: Menor valor possível
    :param limite_superior: Maior valor possível
    :return: Lista de números aleatórios
    """
    print(f"Gerando lista aleatória com {tamanho} elementos...")
    return [random.randint(limite_inferior, limite_superior) for _ in range(tamanho)]

def gerar_entrada_ordenada(tamanho, ordem='crescente'):
    """
    Gera uma lista ordenada (crescente ou decrescente).
    
    :param tamanho: Número de elementos na lista
    :param ordem: 'crescente' ou 'decrescente'
    :return: Lista ordenada
    """
    print(f"Gerando lista {ordem} com {tamanho} elementos...")
    lista = list(range(tamanho))
    return lista if ordem == 'crescente' else list(reversed(lista))

def gerar_entrada_quase_ordenada(tamanho, percentual_desordem=10):
    """
    Gera uma lista quase ordenada com uma porcentagem de elementos fora de ordem.
    
    :param tamanho: Número de elementos na lista
    :param percentual_desordem: Porcentagem de elementos que serão embaralhados
    :return: Lista quase ordenada
    """
    print(f"Gerando lista quase ordenada com {tamanho} elementos ({percentual_desordem}% em desordem)...")
    lista = list(range(tamanho))
    num_desordenados = int(tamanho * percentual_desordem / 100)
    
    # Embaralha uma porção dos elementos
    indices_desordenados = random.sample(range(tamanho), num_desordenados)
    valores_desordenados = [lista[i] for i in indices_desordenados]
    random.shuffle(valores_desordenados)
    
    for i, indice in enumerate(indices_desordenados):
        lista[indice] = valores_desordenados[i]
    
    return lista

def gerar_entrada_com_duplicatas(tamanho, pct_duplicatas=20):
    """
    Gera uma lista com duplicatas.
    
    :param tamanho: Número de elementos na lista
    :param pct_duplicatas: Porcentagem de elementos que serão duplicados
    :return: Lista com duplicatas
    """
    print(f"Gerando lista com {tamanho} elementos ({pct_duplicatas}% duplicatas)...")
    num_valores_unicos = int(tamanho * (1 - pct_duplicatas/100))
    lista_base = list(range(num_valores_unicos))
    
    # Completa o restante com duplicatas
    duplicatas = [random.choice(lista_base) for _ in range(tamanho - num_valores_unicos)]
    lista_final = lista_base + duplicatas
    random.shuffle(lista_final)
    
    return lista_final

def salvar_entrada(lista, nome_arquivo):
    """
    Salva a lista em um arquivo de texto.
    
    :param lista: Lista a ser salva
    :param nome_arquivo: Nome do arquivo de saída
    """
    print(f"Salvando arquivo: {nome_arquivo}")
    with open(nome_arquivo, 'w') as f:
        for num in lista:
            f.write(f"{num}\n")
    print(f"Arquivo {nome_arquivo} salvo com sucesso!")

def main():
    # Tamanhos de entrada para teste - modificados para 10000, 50000, 100000
    tamanhos = [10000, 50000, 100000]
    
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
            nome_arquivo = f'entrada_{nome}_{tamanho}.txt'
            
            # Verifica se o arquivo já existe para evitar regeneração
            if os.path.exists(nome_arquivo):
                print(f"Arquivo {nome_arquivo} já existe, pulando...")
                continue
            
            # Gera entrada
            try:
                inicio = time.time()
                entrada = gerador(tamanho)
                
                # Salva entrada em arquivo
                salvar_entrada(entrada, nome_arquivo)
                
                fim = time.time()
                print(f"Tempo para gerar e salvar {nome_arquivo}: {fim - inicio:.2f} segundos")
            except Exception as e:
                print(f"Erro ao gerar {nome_arquivo}: {e}")

if __name__ == '__main__':
    main()