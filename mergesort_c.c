#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <math.h>  // Para cálculo do desvio padrão

// Função de intercalação
void intercalar(int inicio, int meio, int fim, int v[]) {
    int inicio_v01 = inicio;
    int inicio_v02 = meio + 1;
    int posLivre = 0;
    int* aux = malloc((fim - inicio + 1) * sizeof(int));

    while (inicio_v01 <= meio && inicio_v02 <= fim) {
        if (v[inicio_v01] <= v[inicio_v02]) {
            aux[posLivre++] = v[inicio_v01++];
        } else {
            aux[posLivre++] = v[inicio_v02++];
        }
    }

    while (inicio_v01 <= meio) {
        aux[posLivre++] = v[inicio_v01++];
    }

    while (inicio_v02 <= fim) {
        aux[posLivre++] = v[inicio_v02++];
    }

    for (int i = 0; i < posLivre; i++) {
        v[inicio + i] = aux[i];
    }

    free(aux);
}

// Função merge sort
void mergesort(int inicio, int fim, int v[]) {
    if (inicio < fim) {
        int meio = (inicio + fim) / 2;
        mergesort(inicio, meio, v);
        mergesort(meio + 1, fim, v);
        intercalar(inicio, meio, fim, v);
    }
}

// Função para ler vetor de arquivo
int* ler_vetor_do_arquivo(const char* nome_arquivo, int* tamanho) {
    FILE* arquivo = fopen(nome_arquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s\n", nome_arquivo);
        return NULL;
    }

    // Conta o número de linhas (elementos)
    *tamanho = 0;
    int num;
    while (fscanf(arquivo, "%d", &num) == 1) {
        (*tamanho)++;
    }

    // Retorna para o início do arquivo
    rewind(arquivo);

    // Aloca memória para o vetor
    int* vetor = malloc(*tamanho * sizeof(int));
    if (vetor == NULL) {
        printf("Erro de alocacao de memoria\n");
        fclose(arquivo);
        return NULL;
    }

    // Lê os elementos do arquivo
    for (int i = 0; i < *tamanho; i++) {
        fscanf(arquivo, "%d", &vetor[i]);
    }

    fclose(arquivo);
    return vetor;
}

// Estrutura para armazenar estatísticas
typedef struct {
    double media;
    double desvio_padrao;
    double tempos[30]; // Array para armazenar todos os tempos individuais (máximo 30)
} Estatisticas;

// Função para medir tempo de execução com estatísticas
Estatisticas medir_tempo_execucao(int* vetor, int tamanho, int num_execucoes) {
    Estatisticas stats;
    double soma = 0.0;
    
    // Executa o algoritmo 30 vezes conforme requisito
    for (int r = 0; r < num_execucoes; r++) {
        // Cria uma cópia do vetor para não modificar o original
        int* copia = malloc(tamanho * sizeof(int));
        memcpy(copia, vetor, tamanho * sizeof(int));
        
        clock_t inicio = clock();
        mergesort(0, tamanho - 1, copia);
        clock_t fim = clock();
        
        stats.tempos[r] = ((double)(fim - inicio)) / CLOCKS_PER_SEC;
        soma += stats.tempos[r];
        free(copia);
    }
    
    // Calcula a média
    stats.media = soma / num_execucoes;
    
    // Calcula o desvio padrão
    double soma_quadrados = 0.0;
    for (int r = 0; r < num_execucoes; r++) {
        soma_quadrados += (stats.tempos[r] - stats.media) * (stats.tempos[r] - stats.media);
    }
    stats.desvio_padrao = sqrt(soma_quadrados / num_execucoes);
    
    return stats;
}

// Função principal
int main() {
    // Lista de arquivos de entrada para testar
    const char* arquivos[] = {
        // Tamanhos de entrada: 10.000, 50.000 e 100.000
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
    };
    
    int num_arquivos = sizeof(arquivos) / sizeof(arquivos[0]);
    int num_execucoes = 30;  // Número de execuções: 30

    // Cria arquivo CSV para resultados detalhados
    FILE* resultado_csv = fopen("resultados_mergesort_c_detalhado.csv", "w");
    if (resultado_csv == NULL) {
        printf("Erro ao criar arquivo de resultados CSV\n");
        return 1;
    }
    
    // Cria arquivo CSV para os tempos individuais de cada execução
    FILE* tempos_individuais_csv = fopen("tempos_individuais_mergesort_c.csv", "w");
    if (tempos_individuais_csv == NULL) {
        printf("Erro ao criar arquivo de tempos individuais CSV\n");
        fclose(resultado_csv);
        return 1;
    }
    
    // Cabeçalho do CSV principal
    fprintf(resultado_csv, "Arquivo,Tipo,Tamanho,Media_Tempo(s),Desvio_Padrao(s),Complexidade_Teorica\n");
    
    // Cabeçalho do CSV de tempos individuais
    fprintf(tempos_individuais_csv, "Arquivo,Tipo,Tamanho");
    for (int i = 1; i <= num_execucoes; i++) {
        fprintf(tempos_individuais_csv, ",Execucao_%d", i);
    }
    fprintf(tempos_individuais_csv, "\n");

    // Testa cada arquivo
    for (int i = 0; i < num_arquivos; i++) {
        int tamanho;
        printf("\nCarregando arquivo: %s\n", arquivos[i]);
        int* vetor = ler_vetor_do_arquivo(arquivos[i], &tamanho);
        
        if (vetor == NULL) {
            fprintf(resultado_csv, "%s,erro_leitura,0,0,0,0\n", arquivos[i]);
            continue;
        }

        printf("Analisando arquivo: %s\n", arquivos[i]);
        printf("Tamanho do vetor: %d\n", tamanho);

        // Extrai o tipo de entrada do nome do arquivo
        char tipo[50] = "";
        if (strstr(arquivos[i], "aleatoria") != NULL)
            strcpy(tipo, "aleatoria");
        else if (strstr(arquivos[i], "ordenada_crescente") != NULL)
            strcpy(tipo, "ordenada_crescente");
        else if (strstr(arquivos[i], "ordenada_decrescente") != NULL)
            strcpy(tipo, "ordenada_decrescente");
        else if (strstr(arquivos[i], "quase_ordenada") != NULL)
            strcpy(tipo, "quase_ordenada");
        else if (strstr(arquivos[i], "com_duplicatas") != NULL)
            strcpy(tipo, "com_duplicatas");

        // Mede tempo de execução e calcula estatísticas
        Estatisticas stats = medir_tempo_execucao(vetor, tamanho, num_execucoes);
        
        printf("Tempo médio de execução (%d execuções): %f segundos\n", num_execucoes, stats.media);
        printf("Desvio padrão: %f segundos\n", stats.desvio_padrao);
        
        // Calcula a complexidade teórica (n log n para MergeSort)
        double complexidade_teorica = tamanho * log2(tamanho);
        // Normaliza a complexidade teórica para comparação com tempos medidos
        double fator_escala = stats.media / complexidade_teorica;
        
        // Salva resultados no CSV principal
        fprintf(resultado_csv, "%s,%s,%d,%f,%f,%f\n", 
                arquivos[i], tipo, tamanho, stats.media, stats.desvio_padrao, 
                complexidade_teorica * fator_escala);  // Complexidade teórica escalada
        
        // Salva tempos individuais no CSV de tempos
        fprintf(tempos_individuais_csv, "%s,%s,%d", arquivos[i], tipo, tamanho);
        for (int r = 0; r < num_execucoes; r++) {
            fprintf(tempos_individuais_csv, ",%f", stats.tempos[r]);
        }
        fprintf(tempos_individuais_csv, "\n");

        // Libera memória
        free(vetor);
    }

    fclose(resultado_csv);
    fclose(tempos_individuais_csv);
    printf("\nResultados salvos em resultados_mergesort_c_detalhado.csv\n");  // NOME MODIFICADO
    printf("Tempos individuais salvos em tempos_individuais_mergesort_c.csv\n");  // NOME MODIFICADO

    return 0;
}