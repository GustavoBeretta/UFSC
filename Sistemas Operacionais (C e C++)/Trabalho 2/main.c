#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

typedef struct {
    int *mapa_paginas;
    int tamanho_processo;
} TabelaPaginas;

typedef struct {
    int id_processo;
    TabelaPaginas tabela_paginas;
} Processo;

unsigned char *memoria_fisica;
int *quadros_livres;
Processo *processos;
int num_processos = 0;
int qtd_max_processos;
int num_quadros;
int TAM_MEMORIA_FISICA;
int TAM_PAGINA;
int TAM_MAX_PROCESSO;

bool potencia_de_2(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}

void visualizar_memoria() {
    int quadros_ocupados = 0;

    printf("Memoria Fisica:\n\n");

    for (int i = 0; i < num_quadros; i++) {
        printf("Quadro %d: %s\n", i, quadros_livres[i] ? "Ocupado" : "Livre");

        if (quadros_livres[i]) {
            printf("  Valores: ");
            for (int j = 0; j < TAM_PAGINA; j++) {
                printf("%02X ", memoria_fisica[i * TAM_PAGINA + j]);
            }
            printf("\n");
            quadros_ocupados++;
        }
    }

    float percentual_livre = ((num_quadros - quadros_ocupados) / (float)num_quadros) * 100;
    printf("\nPercentual de memoria livre: %.2f%%\n\n", percentual_livre);
}

void criar_processo() {
    int id_processo, tamanho_processo;
    printf("Informe o ID do processo: ");
    scanf("%d", &id_processo);

    printf("\nDigite o tamanho do processo (em bytes, potencia de 2): ");
    scanf("%d", &tamanho_processo);

    for (int i = 0; i < num_processos; i++) {
        if (processos[i].id_processo == id_processo) {
            printf("\nID do processo ja esta em uso.\n\n");
            return;
        }
    }

    if (!potencia_de_2(tamanho_processo)) {
        printf("\nO tamanho do processo deve ser uma potencia de 2.\n\n");
        return;
    }

    if (tamanho_processo > TAM_MAX_PROCESSO) {
        printf("\nTamanho do processo excede o tamanho maximo permitido.\n\n");
        return;
    }

    int num_paginas = (tamanho_processo + TAM_PAGINA - 1) / TAM_PAGINA;

    int quadros_encontrados = 0;
    for (int i = 0; i < num_quadros; i++) {
        if (quadros_livres[i] == 0) {
            quadros_encontrados++;
        }
        if (quadros_encontrados == num_paginas) break;
    }

    if (quadros_encontrados < num_paginas) {
        printf("\nErro: Memoria insuficiente para alocar o processo.\n\n");
        return;
    }

    int *mapa_paginas = (int *)malloc(num_paginas * sizeof(int));
    int pagina_atual = 0;
    for (int i = 0; i < num_quadros; i++) {
        if (quadros_livres[i] == 0) {
            quadros_livres[i] = 1;
            mapa_paginas[pagina_atual++] = i;
        }
        if (pagina_atual == num_paginas) break;
    }

    for (int i = 0; i < tamanho_processo; i++) {
        int quadro = mapa_paginas[i / TAM_PAGINA];
        int offset = i % TAM_PAGINA;
        memoria_fisica[quadro * TAM_PAGINA + offset] = rand() % 256;
    }

    processos[num_processos].id_processo = id_processo;
    processos[num_processos].tabela_paginas.mapa_paginas = mapa_paginas;
    processos[num_processos].tabela_paginas.tamanho_processo = tamanho_processo;
    num_processos++;

    printf("\nProcesso %d criado com sucesso.\n\n", id_processo);
}

void visualizar_tabela_paginas() {
    int id_processo;
    printf("Informe o ID do processo: ");
    scanf("%d", &id_processo);

    for (int i = 0; i < num_processos; i++) {
        if (processos[i].id_processo == id_processo) {
            TabelaPaginas *tabela = &processos[i].tabela_paginas;
            printf("\nTabela de Paginas do Processo %d:\n\n", id_processo);
            int num_paginas = (tabela->tamanho_processo + TAM_PAGINA - 1) / TAM_PAGINA;
            for (int j = 0; j < num_paginas; j++) {
                printf("Pagina %d -> Quadro %d\n", j, tabela->mapa_paginas[j]);
            }
            printf("\n");
            return;
        }
    }

    printf("\nErro: Processo %d nao encontrado.\n\n", id_processo);
}

int main() {
    srand(time(NULL));

    printf("\n");

    do {
        printf("Digite o tamanho da memoria fisica (em bytes, potencia de 2): ");
        scanf("%d", &TAM_MEMORIA_FISICA);
        if (!potencia_de_2(TAM_MEMORIA_FISICA)) {
            printf("Erro: O tamanho da memoria fisica deve ser uma potencia de 2.\n");
        }
        if (TAM_MEMORIA_FISICA > 128) {
            printf("Erro: O tamanho da memoria fisica deve ser exceder 128B\n");
        }
        printf("\n");
    } while (!potencia_de_2(TAM_MEMORIA_FISICA) || TAM_MEMORIA_FISICA > 128);

    do {
        printf("Digite o tamanho da pagina/quadro (em bytes, potencia de 2): ");
        scanf("%d", &TAM_PAGINA);
        if (!potencia_de_2(TAM_PAGINA)) {
            printf("Erro: O tamanho da pagina/quadro deve ser uma potencia de 2.\n");
        }
        if (TAM_PAGINA > TAM_MEMORIA_FISICA) {
            printf("Erro: O tamanho da pagina/quadro nao pode ser maior que o tamanho da memoria fisica.");
        }
        printf("\n");
    } while (!potencia_de_2(TAM_PAGINA) || TAM_PAGINA > TAM_MEMORIA_FISICA);

    do {
        printf("Digite o tamanho maximo de um processo (em bytes, potencia de 2): ");
        scanf("%d", &TAM_MAX_PROCESSO);
        if (!potencia_de_2(TAM_MAX_PROCESSO)) {
            printf("Erro: O tamanho maximo de um processo deve ser uma potencia de 2.\n");
        }
        if (TAM_MAX_PROCESSO > TAM_MEMORIA_FISICA) {
            printf("Erro: O tamanho maximo de um processo nao pode ser maior que o tamanho da memoria fisica.");
        }
        printf("\n");
    } while (!potencia_de_2(TAM_MAX_PROCESSO) || TAM_MAX_PROCESSO > TAM_MEMORIA_FISICA);

    num_quadros = TAM_MEMORIA_FISICA / TAM_PAGINA;
    qtd_max_processos = num_quadros;

    memoria_fisica = (unsigned char *)calloc(TAM_MEMORIA_FISICA, sizeof(unsigned char));
    quadros_livres = (int *)calloc(num_quadros, sizeof(int));
    
    processos = (Processo *)malloc(qtd_max_processos * sizeof(Processo));

    int opcao;
    do {
        printf("Opcoes:\n\n");
        printf("1. Visualizar memoria\n");
        printf("2. Criar processo\n");
        printf("3. Visualizar tabela de paginas\n");
        printf("0. Sair\n\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);
        printf("\n");

        switch (opcao) {
            case 1:
                visualizar_memoria();
                break;
            case 2:
                criar_processo();
                break;
            case 3:
                visualizar_tabela_paginas();
                break;
            case 0:
                printf("Encerrando o programa.\n\n");
                break;
            default:
                printf("Opção inválida. Tente novamente.\n\n");
        }
    } while (opcao != 0);

    free(memoria_fisica);
    free(quadros_livres);
    for (int i = 0; i < num_processos; i++) {
        free(processos[i].tabela_paginas.mapa_paginas);
    }
    free(processos);

    return 0;
}