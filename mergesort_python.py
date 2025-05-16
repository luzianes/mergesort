import time
import math
import statistics
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Implementação do MergeSort em Python
def merge(arr, inicio, meio, fim):
    # Cria arrays temporários
    parte1 = arr[inicio:meio+1]
    parte2 = arr[meio+1:fim+1]
    
    # Índices para percorrer os arrays
    i = j = 0
    k = inicio
    
    # Mescla os arrays temporários de volta no array original
    while i < len(parte1) and j < len(parte2):
        if parte1[i] <= parte2[j]:
            arr[k] = parte1[i]
            i += 1
        else:
            arr[k] = parte2[j]
            j += 1
        k += 1
    
    # Copia os elementos restantes de parte1[], se houver
    while i < len(parte1):
        arr[k] = parte1[i]
        i += 1
        k += 1
    
    # Copia os elementos restantes de parte2[], se houver
    while j < len(parte2):
        arr[k] = parte2[j]
        j += 1
        k += 1

def mergesort(arr, inicio, fim):
    if inicio < fim:
        meio = (inicio + fim) // 2
        
        # Ordena as duas metades
        mergesort(arr, inicio, meio)
        mergesort(arr, meio + 1, fim)
        
        # Mescla as metades ordenadas
        merge(arr, inicio, meio, fim)

# Função para ler vetor do arquivo
def ler_vetor_do_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        vetor = [int(linha.strip()) for linha in f]
    return vetor

# Função para medir o tempo de execução
def medir_tempo_execucao(vetor, num_execucoes=30):
    tempos = []
    
    for _ in range(num_execucoes):
        # Cria uma cópia do vetor para não modificar o original
        copia = vetor.copy()
        
        # Mede o tempo
        inicio = time.time()
        mergesort(copia, 0, len(copia) - 1)
        fim = time.time()
        
        tempos.append(fim - inicio)
    
    # Calcula estatísticas
    media = statistics.mean(tempos)
    desvio_padrao = statistics.stdev(tempos) if len(tempos) > 1 else 0
    
    return {
        'media': media,
        'desvio_padrao': desvio_padrao,
        'tempos': tempos
    }

# Função principal
def main():
    # Lista de arquivos de entrada para testar
    arquivos = [
        # Tamanhos de entrada: 10.000, 50.000 e 100.000
        "entrada_aleatoria_10000.txt",
        "entrada_aleatoria_50000.txt",
        "entrada_aleatoria_100000.txt",
        "entrada_ordenada_crescente_10000.txt",
        "entrada_ordenada_crescente_50000.txt",
        "entrada_ordenada_crescente_100000.txt",
        "entrada_ordenada_decrescente_10000.txt",
        "entrada_ordenada_decrescente_50000.txt",
        "entrada_ordenada_decrescente_100000.txt",
        "entrada_quase_ordenada_10000.txt",
        "entrada_quase_ordenada_50000.txt",
        "entrada_quase_ordenada_100000.txt",
        "entrada_com_duplicatas_10000.txt",
        "entrada_com_duplicatas_50000.txt",
        "entrada_com_duplicatas_100000.txt"
    ]
    
    num_execucoes = 30  # Número de execuções para média/desvio padrão
    
    # Preparar dataframes para resultados
    resultados = []
    tempos_individuais = []
    
    # Testa cada arquivo
    for arquivo in arquivos:
        print(f"\nCarregando arquivo: {arquivo}")
        
        # Verifica se o arquivo existe
        if not os.path.exists(arquivo):
            print(f"Arquivo {arquivo} não encontrado!")
            continue
        
        vetor = ler_vetor_do_arquivo(arquivo)
        
        print(f"Analisando arquivo: {arquivo}")
        print(f"Tamanho do vetor: {len(vetor)}")
        
        # Extrai o tipo de entrada do nome do arquivo
        tipo = ""
        if "aleatoria" in arquivo:
            tipo = "aleatoria"
        elif "ordenada_crescente" in arquivo:
            tipo = "ordenada_crescente"
        elif "ordenada_decrescente" in arquivo:
            tipo = "ordenada_decrescente"
        elif "quase_ordenada" in arquivo:
            tipo = "quase_ordenada"
        elif "com_duplicatas" in arquivo:
            tipo = "com_duplicatas"
        
        # Mede tempo de execução e calcula estatísticas
        stats = medir_tempo_execucao(vetor, num_execucoes)
        
        print(f"Tempo médio de execução ({num_execucoes} execuções): {stats['media']} segundos")
        print(f"Desvio padrão: {stats['desvio_padrao']} segundos")
        
        # Calcula a complexidade teórica (n log n para MergeSort)
        tamanho = len(vetor)
        complexidade_teorica = tamanho * math.log2(tamanho)
        
        # Normaliza a complexidade teórica para comparação com tempos medidos
        fator_escala = stats['media'] / complexidade_teorica
        
        # Adiciona aos resultados
        resultados.append({
            'Arquivo': arquivo,
            'Tipo': tipo,
            'Tamanho': tamanho,
            'Media_Tempo(s)': stats['media'],
            'Desvio_Padrao(s)': stats['desvio_padrao'],
            'Complexidade_Teorica': complexidade_teorica * fator_escala
        })
        
        # Adiciona tempos individuais
        tempo_individual = {
            'Arquivo': arquivo,
            'Tipo': tipo,
            'Tamanho': tamanho
        }
        for i, tempo in enumerate(stats['tempos']):
            tempo_individual[f'Execucao_{i+1}'] = tempo
        
        tempos_individuais.append(tempo_individual)
    
    # Cria DataFrames a partir das listas
    df_resultados = pd.DataFrame(resultados)
    df_tempos = pd.DataFrame(tempos_individuais)
    
    # Salva os resultados em arquivos CSV
    df_resultados.to_csv('resultados_mergesort_python_detalhado.csv', index=False)
    df_tempos.to_csv('tempos_individuais_mergesort_python.csv', index=False)
    
    print("\nResultados salvos em resultados_mergesort_python_detalhado.csv")
    print("Tempos individuais salvos em tempos_individuais_mergesort_python.csv")

if __name__ == "__main__":
    main()