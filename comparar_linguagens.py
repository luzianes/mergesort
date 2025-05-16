import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função para carregar dados dos resultados - NOMES MODIFICADOS
def carregar_dados(arquivo_c='resultados_mergesort_c_detalhado.csv', 
                   arquivo_python='resultados_mergesort_python_detalhado.csv'):
    try:
        df_c = pd.read_csv(arquivo_c)
        df_python = pd.read_csv(arquivo_python)
        return df_c, df_python
    except Exception as e:
        print(f"Erro ao carregar arquivos: {e}")
        return None, None

# Gráfico de comparação entre C e Python para cada tipo e tamanho
def comparar_c_python(df_c, df_python):
    # Garantir que os DataFrames estão combinados corretamente
    df_c['Linguagem'] = 'C'
    df_python['Linguagem'] = 'Python'
    
    # Combinar os dados
    df_combinado = pd.concat([df_c, df_python])
    
    # Agrupar por tipo, tamanho e linguagem
    df_agrupado = df_combinado.groupby(['Tipo', 'Tamanho', 'Linguagem']).agg({
        'Media_Tempo(s)': 'mean',
        'Desvio_Padrao(s)': 'mean'
    }).reset_index()
    
    # Criar gráficos para cada tipo
    tipos = df_agrupado['Tipo'].unique()
    tamanhos = sorted(df_agrupado['Tamanho'].unique())
    
    # Configurar figura
    fig, axes = plt.subplots(len(tipos), 1, figsize=(12, 4*len(tipos)))
    
    for i, tipo in enumerate(tipos):
        df_tipo = df_agrupado[df_agrupado['Tipo'] == tipo]
        
        # Organizar dados para plotagem
        df_c_tipo = df_tipo[df_tipo['Linguagem'] == 'C']
        df_python_tipo = df_tipo[df_tipo['Linguagem'] == 'Python']
        
        # Plotar barras
        ax = axes[i] if len(tipos) > 1 else axes
        x = np.arange(len(tamanhos))
        width = 0.35
        
        rects1 = ax.bar(x - width/2, df_c_tipo.sort_values('Tamanho')['Media_Tempo(s)'], 
                        width, label='C', yerr=df_c_tipo.sort_values('Tamanho')['Desvio_Padrao(s)'],
                        capsize=5)
        rects2 = ax.bar(x + width/2, df_python_tipo.sort_values('Tamanho')['Media_Tempo(s)'], 
                        width, label='Python', yerr=df_python_tipo.sort_values('Tamanho')['Desvio_Padrao(s)'],
                        capsize=5)
        
        # Adicionar labels e títulos
        ax.set_xlabel('Tamanho da Entrada')
        ax.set_ylabel('Tempo (s)')
        ax.set_title(f'Comparação C vs Python - Tipo: {tipo}')
        ax.set_xticks(x)
        ax.set_xticklabels(tamanhos)
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Adicionar valores nas barras
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f'{height:.4f}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 pts vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', rotation=90)
        
        autolabel(rects1)
        autolabel(rects2)
    
    plt.tight_layout()
    plt.savefig('comparacao_c_vs_python.png')
    plt.close()

# Gráfico de aceleração (speedup) do C em relação ao Python
def calcular_speedup(df_c, df_python):
    # Mesclar os DataFrames para calcular o speedup
    df_merged = pd.merge(df_c, df_python, 
                         on=['Tipo', 'Tamanho'], 
                         suffixes=('_c', '_python'))
    
    # Calcular speedup
    df_merged['Speedup'] = df_merged['Media_Tempo(s)_python'] / df_merged['Media_Tempo(s)_c']
    
    # Agrupar por tipo e tamanho
    df_speedup = df_merged.groupby(['Tipo', 'Tamanho']).agg({
        'Speedup': 'mean'
    }).reset_index()
    
    # Criar gráfico de barras para o speedup
    plt.figure(figsize=(12, 6))
    
    tipos = df_speedup['Tipo'].unique()
    tamanhos = sorted(df_speedup['Tamanho'].unique())
    
    # Cores para diferentes tipos
    colors = plt.cm.viridis(np.linspace(0, 1, len(tipos)))
    
    # Posições das barras
    bar_width = 0.15
    index = np.arange(len(tamanhos))
    
    for i, tipo in enumerate(tipos):
        df_tipo = df_speedup[df_speedup['Tipo'] == tipo]
        df_tipo = df_tipo.sort_values('Tamanho')
        
        plt.bar(index + i*bar_width, df_tipo['Speedup'], bar_width,
                label=tipo, color=colors[i])
    
    plt.xlabel('Tamanho da Entrada')
    plt.ylabel('Speedup (Python / C)')
    plt.title('Speedup de Python em relação a C')
    plt.xticks(index + bar_width*(len(tipos)-1)/2, tamanhos)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Linha de referência para speedup = 1 (mesma velocidade)
    plt.axhline(y=1, color='r', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('speedup_python_vs_c.png')
    plt.close()

# Função principal
def main():
    # Carregar dados
    df_c, df_python = carregar_dados()
    
    if df_c is None or df_python is None:
        print("Erro ao carregar os dados. Verifique se os arquivos CSV existem.")
        return
    
    # Gerar gráficos comparativos
    comparar_c_python(df_c, df_python)
    
    # Calcular e plotar speedup
    calcular_speedup(df_c, df_python)
    
    print("Gráficos comparativos gerados com sucesso!")

if __name__ == "__main__":
    main()