#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Função de intercalação (mantida igual ao código anterior)
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

// Função merge sort (mantida igual)
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
        printf("Erro de alocação de memória\n");
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

// Função para medir tempo de execução
double medir_tempo_execucao(int* vetor, int tamanho) {
    clock_t inicio, fim;
    
    // Cria uma cópia do vetor para não modificar o original
    int* copia = malloc(tamanho * sizeof(int));
    for (int i = 0; i < tamanho; i++) {
        copia[i] = vetor[i];
    }
    
    inicio = clock();
    mergesort(0, tamanho - 1, copia);
    fim = clock();
    
    free(copia);
    return ((double)(fim - inicio)) / CLOCKS_PER_SEC;
}

// Função para imprimir vetor
void imprimir_vetor(int* vetor, int tamanho) {
    for (int i = 0; i < tamanho; i++) {
        printf("%d ", vetor[i]);
    }
    printf("\n");
}

// Função principal
int main() {
    // Lista de arquivos de entrada para testar
    const char* arquivos[] = {
        "entrada_aleatoria_100.txt",
        "entrada_aleatoria_1000.txt",
        "entrada_aleatoria_10000.txt",
        "entrada_ordenada_crescente_100.txt",
        "entrada_ordenada_decrescente_100.txt",
        "entrada_quase_ordenada_100.txt",
        "entrada_com_duplicatas_100.txt"
    };
    
    int num_arquivos = sizeof(arquivos) / sizeof(arquivos[0]);

    // Testa cada arquivo
    for (int i = 0; i < num_arquivos; i++) {
        int tamanho;
        int* vetor = ler_vetor_do_arquivo(arquivos[i], &tamanho);
        
        if (vetor == NULL) {
            continue;
        }

        printf("\nAnalisando arquivo: %s\n", arquivos[i]);
        printf("Tamanho do vetor: %d\n", tamanho);

        // Mede tempo de execução
        double tempo = medir_tempo_execucao(vetor, tamanho);
        
        printf("Tempo de execução: %f segundos\n", tempo);

        // Libera memória
        free(vetor);
    }

    return 0;
}