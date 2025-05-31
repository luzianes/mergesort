# Análise de Complexidade Temporal do Merge Sort

## 📋 Descrição do Projeto

Este projeto implementa e analisa o algoritmo **Merge Sort** em duas linguagens de programação (C e Python), realizando uma análise detalhada da complexidade temporal e comparação de performance entre as implementações.

### 🎯 Objetivos
- Implementar o algoritmo Merge Sort em C e Python
- Analisar a complexidade temporal teórica vs. prática
- Comparar performance entre as duas linguagens
- Avaliar comportamento em diferentes tipos de entrada
- Gerar gráficos comparativos e análises estatísticas

## 🚀 Como Executar

### Pré-requisitos
- **Python 3.11+** com as bibliotecas:
  - pandas 2.2.2
  - matplotlib 3.10.3
  - numpy 2.0.1
  - statistics (biblioteca padrão)
  - time (biblioteca padrão)
- **GCC** para compilação do código C
- **Sistema Windows** (testado no Windows 11)

### Execução Completa
Execute os comandos na seguinte ordem:

```bash
# 1. Gerar entradas de teste
python gerar_entradas.py

# 2. Compilar e executar implementação em C
gcc mergesort_c.c -o mergesort_c -lm
./mergesort_c

# 3. Executar implementação em Python
python mergesort_python.py

# 4. Gerar gráficos individuais por linguagem
python gerar_graficos.py both

# 5. Gerar gráficos comparativos entre linguagens
python comparar_linguagens.py
```

## 🔬 Metodologia Experimental

### Tipos de Entrada
- **Aleatória**: Números inteiros aleatórios (0 a 1.000.000)
- **Ordenada Crescente**: Sequência 0 a n-1
- **Ordenada Decrescente**: Sequência n-1 a 0
- **Quase Ordenada**: 90% ordenada, 10% embaralhada
- **Com Duplicatas**: 20% de valores duplicados

### Tamanhos de Entrada
- **Pequeno**: 10.000 elementos
- **Médio**: 50.000 elementos
- **Grande**: 100.000 elementos

### Execuções
- **30 repetições** por combinação de tipo/tamanho
- Cálculo de média e desvio padrão
- Análise estatística dos resultados

## 📊 Resultados Esperados

### Gráficos Gerados
1. **Comparação por tipos de entrada** (C e Python separadamente)
2. **Tempo vs. Complexidade teórica** (validação O(n log n))
3. **Crescimento por tamanho** para cada tipo
4. **Comparação direta C vs Python**
5. **Análise de speedup** (quantas vezes C é mais rápido)

### Arquivos de Saída
- `resultados_mergesort_c_detalhado.csv`
- `resultados_mergesort_python_detalhado.csv`
- `tempos_individuais_mergesort_c.csv`
- `tempos_individuais_mergesort_python.csv`
- Vários arquivos `.png` com os gráficos

## 🔧 Ambiente de Teste

- **SO**: Microsoft Windows 11 Home Single Language
- **Processador**: Intel Core i7-1255U (12ª geração)
- **RAM**: 16 GB
- **Compilador**: GCC 6.3.0 (MinGW)
- **Python**: 3.11.5

## 📈 Resultados Principais

### Complexidade Confirmada
- ✅ **O(n log n)** em todos os casos (melhor, médio, pior)
- ✅ Comportamento consistente independente do tipo de entrada
- ✅ Crescimento temporal segue curva teórica esperada

### Performance C vs Python
- 🏆 **C é ~8-19x mais rápido** que Python
- ⚡ Speedup varia conforme tamanho da entrada
- 📊 Diferença mais pronunciada em entradas maiores

## 🎓 Contexto Acadêmico

Este projeto foi desenvolvido para a disciplina **Teoria da Computação** como análise prática de complexidade de algoritmos, demonstrando:

- Análise assintótica (Big-O, Ω, Θ)
- Metodologia experimental sistemática
- Comparação entre linguagens de programação
- Validação empírica de análise teórica

## 👥 Equipe

- [@lilymtbr](https://github.com/lilymtbr) - Lisa Matubara
- [@luzianes](https://github.com/luzianes) - Luziane Santos
  
## 📝 Licença

Este projeto é para fins educacionais como parte do curso de Teoria da Computação.

---

**Data**: 01 Julho 2025  
**Instituição**: CESAR School  
**Disciplina**: Teoria da Computação
