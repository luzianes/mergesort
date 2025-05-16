import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

# Função para carregar dados e gerar gráficos
def gerar_graficos(linguagem="c"):
    # Determina os nomes dos arquivos baseado na linguagem
    if linguagem.lower() == "c":
        arquivo_csv = 'resultados_mergesort_c_detalhado.csv'
        sufixo_saida = '_c'
        titulo_linguagem = ' (C)'
    elif linguagem.lower() == "python":
        arquivo_csv = 'resultados_mergesort_python_detalhado.csv'
        sufixo_saida = '_python'
        titulo_linguagem = ' (Python)'
    else:
        print(f"Linguagem '{linguagem}' não reconhecida. Use 'c' ou 'python'.")
        return

    # Carrega os dados do CSV
    try:
        df = pd.read_csv(arquivo_csv)
    except Exception as e:
        print(f"Erro ao carregar o arquivo {arquivo_csv}: {e}")
        return None

    # Cria gráfico de barras comparando tempos médios para diferentes tipos de entrada
    def grafico_barras_tipos():
        # Agrupar por tipo e tamanho, calculando a média do tempo
        df_agrupado = df.groupby(['Tipo', 'Tamanho']).agg({
            'Media_Tempo(s)': 'mean',
            'Desvio_Padrao(s)': 'mean'
        }).reset_index()
        
        # Separar os dados por tamanho
        tamanhos_unicos = df['Tamanho'].unique()
        tipos_unicos = df['Tipo'].unique()
        
        # Configurar gráfico com tamanho maior
        fig, axs = plt.subplots(1, len(tamanhos_unicos), figsize=(20, 6), sharey=True)
        
        # Posições e largura das barras
        width = 0.7  # Barras mais largas
        
        # Criar dicionário para nomes mais curtos e claros
        nomes_tipos = {
            'aleatoria': 'Aleatória',
            'com_duplicatas': 'Duplicatas',
            'ordenada_crescente': 'Crescente',
            'ordenada_decrescente': 'Decrescente',
            'quase_ordenada': 'Quase Ord.'
        }
        
        for i, tamanho in enumerate(sorted(tamanhos_unicos)):
            dados_tamanho = df_agrupado[df_agrupado['Tamanho'] == tamanho]
            
            # Ordenar por tipo para manter a mesma ordem em todos os gráficos
            dados_tamanho = dados_tamanho.sort_values('Tipo')
            
            # Preparar nomes curtos para exibição
            nomes_curtos = [nomes_tipos.get(tipo, tipo) for tipo in dados_tamanho['Tipo']]
            
            # Criar barras com tempos médios
            barras = axs[i].bar(nomes_curtos, dados_tamanho['Media_Tempo(s)'], width, 
                               yerr=dados_tamanho['Desvio_Padrao(s)'], 
                               capsize=5)
            
            # Adicionar rótulos de valor nas barras
            for barra in barras:
                altura = barra.get_height()
                axs[i].text(barra.get_x() + barra.get_width()/2., altura + 0.0005,
                           f'{altura:.5f}',
                           ha='center', va='bottom', fontsize=8, rotation=0)
            
            axs[i].set_title(f'Tamanho: {tamanho}')
            axs[i].set_ylabel('Tempo (s)')
            
            # Melhorar posicionamento dos rótulos do eixo x
            plt.setp(axs[i].get_xticklabels(), rotation=45, ha='right')
            
            # Adicionar grade para melhor visualização
            axs[i].grid(axis='y', linestyle='--', alpha=0.7)
        
        # Adicionar título principal
        fig.suptitle(f'Comparação de Tempos para Diferentes Tipos de Entrada{titulo_linguagem}', 
                     fontsize=16, y=1.05)
        
        # Aumentar espaço na parte inferior para rótulos
        plt.subplots_adjust(bottom=0.2, wspace=0.1, top=0.85)
        
        plt.tight_layout()
        plt.savefig(f'comparacao_tipos_entrada{sufixo_saida}.png', bbox_inches='tight', dpi=300)
        plt.close()

    # Cria gráfico de linha comparando crescimento do tempo vs. complexidade teórica
    def grafico_complexidade():
        # Agrupar por tamanho, calculando as médias
        df_por_tamanho = df.groupby('Tamanho').agg({
            'Media_Tempo(s)': 'mean',
            'Complexidade_Teorica': 'mean'
        }).reset_index()
        
        # Ordenar por tamanho
        df_por_tamanho = df_por_tamanho.sort_values('Tamanho')
        
        # Criar gráfico
        plt.figure(figsize=(10, 6))
        
        # Plotar tempos medidos
        plt.plot(df_por_tamanho['Tamanho'], df_por_tamanho['Media_Tempo(s)'], 
                'o-', label='Tempo Medido', linewidth=2, markersize=8)
        
        # Plotar complexidade teórica (n log n)
        plt.plot(df_por_tamanho['Tamanho'], df_por_tamanho['Complexidade_Teorica'], 
                's--', label='Complexidade Teórica (n log n)', linewidth=2, markersize=8)
        
        # Adicionar rótulos para cada ponto de dados
        for i, row in df_por_tamanho.iterrows():
            plt.annotate(f'{row["Media_Tempo(s)"]:.5f}s', 
                        (row['Tamanho'], row['Media_Tempo(s)']),
                        textcoords="offset points", 
                        xytext=(0,10), 
                        ha='center')
        
        plt.xlabel('Tamanho da Entrada (n)', fontsize=12)
        plt.ylabel('Tempo (s)', fontsize=12)
        plt.title(f'Tempo de Execução vs. Complexidade Teórica{titulo_linguagem}', fontsize=14)
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Melhorar estilo do gráfico
        plt.tight_layout()
        plt.savefig(f'tempo_vs_complexidade{sufixo_saida}.png', dpi=300)
        plt.close()

    # Cria gráfico de barras para diferentes tamanhos por tipo de entrada
    def grafico_tamanhos_por_tipo():
        # Agrupar por tipo e tamanho
        tipos_unicos = df['Tipo'].unique()
        
        # Dicionário para nomes mais amigáveis
        nomes_tipos = {
            'aleatoria': 'Aleatória',
            'com_duplicatas': 'Com Duplicatas',
            'ordenada_crescente': 'Ordenada Crescente',
            'ordenada_decrescente': 'Ordenada Decrescente',
            'quase_ordenada': 'Quase Ordenada'
        }
        
        # Criar gráfico para cada tipo
        plt.figure(figsize=(12, 10))
        
        for i, tipo in enumerate(tipos_unicos):
            df_tipo = df[df['Tipo'] == tipo]
            df_tipo = df_tipo.sort_values('Tamanho')
            
            plt.subplot(len(tipos_unicos), 1, i+1)
            barras = plt.bar(df_tipo['Tamanho'].astype(str), df_tipo['Media_Tempo(s)'], 
                           width=0.7,
                           yerr=df_tipo['Desvio_Padrao(s)'], 
                           capsize=5)
            
            # Adicionar rótulos de valores nas barras
            for barra in barras:
                altura = barra.get_height()
                plt.text(barra.get_x() + barra.get_width()/2., altura + altura*0.01,
                       f'{altura:.5f}s',
                       ha='center', va='bottom', fontsize=8)
            
            plt.ylabel('Tempo (s)', fontsize=10)
            plt.title(f'Tipo: {nomes_tipos.get(tipo, tipo)}{titulo_linguagem}', fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Ajustar os rótulos do eixo x para evitar sobreposição
            plt.xticks(fontsize=10)
            
            # Adicionar uma linha de tendência suave
            x_num = np.arange(len(df_tipo))
            z = np.polyfit(x_num, df_tipo['Media_Tempo(s)'], 2)
            p = np.poly1d(z)
            plt.plot(df_tipo['Tamanho'].astype(str), p(x_num), "r--", alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(f'tamanhos_por_tipo{sufixo_saida}.png', dpi=300)
        plt.close()

    # Gerar todos os gráficos
    grafico_barras_tipos()
    grafico_complexidade()
    grafico_tamanhos_por_tipo()
    
    print(f"Gráficos para {linguagem.upper()} gerados com sucesso!")

def main():
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Gera gráficos para análise do MergeSort.')
    parser.add_argument('linguagem', type=str, choices=['c', 'python', 'both'], 
                      default='both', nargs='?',
                      help='Linguagem para gerar gráficos (c, python ou both)')
    
    args = parser.parse_args()
    
    # Gerar gráficos com base na linguagem especificada
    if args.linguagem == 'both':
        gerar_graficos('c')
        gerar_graficos('python')
    else:
        gerar_graficos(args.linguagem)

if __name__ == "__main__":
    main()