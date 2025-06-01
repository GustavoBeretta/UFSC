#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <string.h>
#include <time.h>

#define NUM_CLIENTES 100
#define MAX_CAIXAS_ATIVOS 2
#define NUM_THREADS 4

typedef struct {
    int id;
    int preferencial;
} Cliente;

typedef struct Tarefa {
    int id_cliente;
    int id_caixa;
    double tempo_atendimento;
    struct Tarefa* prox;
} Tarefa;

Cliente* fila_prioritaria[NUM_CLIENTES];
Cliente* fila_comum[NUM_CLIENTES];
int ini_p = 0, fim_p = 0;
int ini_c = 0, fim_c = 0;

Tarefa* fila_tarefas = NULL;
Tarefa* fim_tarefa = NULL;

Tarefa* relatorio_final = NULL;
Tarefa* fim_rel_final = NULL;

pthread_mutex_t mutex_filas = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex_tarefa = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond_tarefa = PTHREAD_COND_INITIALIZER;
sem_t sem_caixas;

int clientes_restantes = NUM_CLIENTES;

void enfileira_cliente(Cliente* c) {
    pthread_mutex_lock(&mutex_filas);
    if (c->preferencial)
        fila_prioritaria[fim_p++] = c;
    else
        fila_comum[fim_c++] = c;
    pthread_mutex_unlock(&mutex_filas);
}

Cliente* desenfileira_cliente() {
    pthread_mutex_lock(&mutex_filas);
    Cliente* c = NULL;
    if (ini_p < fim_p)
        c = fila_prioritaria[ini_p++];
    else if (ini_c < fim_c)
        c = fila_comum[ini_c++];
    pthread_mutex_unlock(&mutex_filas);
    return c;
}

void enfileira_tarefa(int id_cliente, int id_caixa, double tempo) {
    Tarefa* nova = malloc(sizeof(Tarefa));
    nova->id_cliente = id_cliente;
    nova->id_caixa = id_caixa;
    nova->tempo_atendimento = tempo;
    nova->prox = NULL;

    pthread_mutex_lock(&mutex_tarefa);
    if (fim_tarefa)
        fim_tarefa->prox = nova;
    else
        fila_tarefas = nova;
    fim_tarefa = nova;

    Tarefa* nova_final = malloc(sizeof(Tarefa));
    nova_final->id_cliente = id_cliente;
    nova_final->id_caixa = id_caixa;
    nova_final->tempo_atendimento = tempo;
    nova_final->prox = NULL;

    if (fim_rel_final)
        fim_rel_final->prox = nova_final;
    else
        relatorio_final = nova_final;
    fim_rel_final = nova_final;

    pthread_cond_signal(&cond_tarefa);
    pthread_mutex_unlock(&mutex_tarefa);
}

Tarefa* desenfileira_tarefa() {
    pthread_mutex_lock(&mutex_tarefa);
    while (fila_tarefas == NULL && clientes_restantes > 0) {
        pthread_cond_wait(&cond_tarefa, &mutex_tarefa);
    }
    if (fila_tarefas == NULL && clientes_restantes <= 0) {
        pthread_mutex_unlock(&mutex_tarefa);
        return NULL;
    }

    Tarefa* t = fila_tarefas;
    fila_tarefas = fila_tarefas->prox;
    if (!fila_tarefas)
        fim_tarefa = NULL;
    pthread_mutex_unlock(&mutex_tarefa);
    return t;
}

int cmp_tarefa(const void* a, const void* b) {
    const Tarefa* t1 = *(const Tarefa**)a;
    const Tarefa* t2 = *(const Tarefa**)b;
    return t1->id_cliente - t2->id_cliente;
}

void* thread_func(void* arg) {
    int id = *(int*)arg;
    char nome_arquivo[32];
    sprintf(nome_arquivo, "relatorio_thread_%d.txt", id);
    FILE* f = fopen(nome_arquivo, "w");
    if (!f) pthread_exit(NULL);

    while (1) {
        if (sem_trywait(&sem_caixas) == 0) {
            Cliente* c = desenfileira_cliente();
            if (c) {
                printf("[Thread %d] Atendendo cliente %d (%s)\n", id, c->id, c->preferencial ? "PREFERENCIAL" : "comum");
                struct timespec start, end;
                clock_gettime(CLOCK_MONOTONIC, &start);
                sleep(rand() % 5 + 1);
                clock_gettime(CLOCK_MONOTONIC, &end);
                double tempo = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

                enfileira_tarefa(c->id, id, tempo);

                printf("[Thread %d] Finalizou cliente %d em %.3f segundos\n", id, c->id, tempo);
                free(c);

                pthread_mutex_lock(&mutex_tarefa);
                clientes_restantes--;
                if (clientes_restantes == 0) {
                    pthread_cond_broadcast(&cond_tarefa);
                }
                pthread_mutex_unlock(&mutex_tarefa);
            }
            sem_post(&sem_caixas);
        }

        pthread_mutex_lock(&mutex_tarefa);
        while (fila_tarefas == NULL && clientes_restantes > 0) {
            pthread_cond_wait(&cond_tarefa, &mutex_tarefa);
        }

        if (fila_tarefas == NULL && clientes_restantes <= 0) {
            pthread_mutex_unlock(&mutex_tarefa);
            break;
        }

        Tarefa* t = fila_tarefas;
        fila_tarefas = fila_tarefas->prox;
        if (!fila_tarefas)
            fim_tarefa = NULL;
        pthread_mutex_unlock(&mutex_tarefa);

        fprintf(f, "Cliente %d atendido pelo caixa %d em %.3f segundos\n", t->id_cliente, t->id_caixa, t->tempo_atendimento);
        printf("[Thread %d] Gravou relatório do cliente %d\n", id, t->id_cliente);
        free(t);

        usleep(10000);
    }

    fclose(f);
    printf("[Thread %d] Encerrando.\n", id);
    return NULL;
}

int main() {
    srand(time(NULL));
    sem_init(&sem_caixas, 0, MAX_CAIXAS_ATIVOS);

    for (int i = 0; i < NUM_CLIENTES; i++) {
        Cliente* c = malloc(sizeof(Cliente));
        c->id = i + 1;
        c->preferencial = rand() % 5 == 0;
        enfileira_cliente(c);
    }

    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];
    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i + 1;
        pthread_create(&threads[i], NULL, thread_func, &ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    int count = 0;
    for (Tarefa* cur = relatorio_final; cur != NULL; cur = cur->prox)
        count++;

    if (count > 0) {
        Tarefa** arr = malloc(count * sizeof(Tarefa*));
        int idx = 0;
        for (Tarefa* cur = relatorio_final; cur != NULL; cur = cur->prox)
            arr[idx++] = cur;

        qsort(arr, count, sizeof(Tarefa*), cmp_tarefa);

        FILE* ffinal = fopen("relatorio_final_ordenado.txt", "w");
        if (ffinal) {
            for (int i = 0; i < count; i++) {
                fprintf(ffinal, "Cliente %d atendido pelo caixa %d em %.3f segundos\n",
                    arr[i]->id_cliente, arr[i]->id_caixa, arr[i]->tempo_atendimento);
            }
            fclose(ffinal);
        }
        free(arr);
    }

    sem_destroy(&sem_caixas);
    pthread_mutex_destroy(&mutex_filas);
    pthread_mutex_destroy(&mutex_tarefa);
    pthread_cond_destroy(&cond_tarefa);

    printf("\n[Main] Todos os atendimentos e relatórios finalizados.\n");
    return 0;
}