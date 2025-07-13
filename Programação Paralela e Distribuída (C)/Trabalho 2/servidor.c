#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <stdint.h>

#define BASE_PORT 15700
#define MAX_BUFFER_SIZE 8192
#define MAX_CONEXOES 20

#define SUCESSO 0
#define ERRO_MEMORIA_INEXISTENTE -2
#define ERRO_COMANDO_DESCONHECIDO -3
#define ERRO_FALHA_OBTER_BLOCO -4

#define CMD_OBTER_DADOS 1
#define CMD_SALVAR_DADOS 2
#define CMD_OBTER_BLOCO_INTERNO 3
#define CMD_ATUALIZAR_BLOCO 4
#define CMD_INVALIDAR_BLOCO 5

typedef struct
{
    int id;
    char *dados;
} BlocoMemoria;

typedef struct
{
    int id;
    char *dados;
    int valido;
} BlocoCache;

int N_PROCESSOS = 0, K_BLOCOS = 0, T_BLOCO = 0, my_rank = 0;
BlocoMemoria *blocos_locais = NULL;
int num_blocos_locais = 0;
BlocoCache *cache = NULL;
int tamanho_cache = 0, proximo_slot_cache = 0;
pthread_mutex_t cache_mutex;

void die(const char *msg)
{
    perror(msg);
    exit(EXIT_FAILURE);
}

int recv_all(int sock, char *buffer, int len)
{
    int total_recebido = 0;
    while (total_recebido < len)
    {
        int bytes_recebidos = recv(sock, buffer + total_recebido, len - total_recebido, 0);
        if (bytes_recebidos <= 0)
            return -1;
        total_recebido += bytes_recebidos;
    }
    return total_recebido;
}

int calcular_dono(int id_bloco)
{
    if (id_bloco < 0 || id_bloco >= K_BLOCOS)
        return -1;
    if (N_PROCESSOS == 0)
        return -1;
    int blocos_por_processo = K_BLOCOS / N_PROCESSOS;
    if (blocos_por_processo == 0)
    {
        return (id_bloco < K_BLOCOS) ? id_bloco % N_PROCESSOS : -1;
    }
    int dono = id_bloco / blocos_por_processo;
    return (dono >= N_PROCESSOS) ? N_PROCESSOS - 1 : dono;
}

void mapear_posicao_global(int p, int *id, int *off)
{
    *id = p / T_BLOCO;
    *off = p % T_BLOCO;
}

const char *traduzir_comando(int comando)
{
    switch (comando)
    {
    case CMD_OBTER_DADOS:
        return "OBTER_DADOS";
    case CMD_SALVAR_DADOS:
        return "SALVAR_DADOS";
    case CMD_OBTER_BLOCO_INTERNO:
        return "OBTER_BLOCO_INTERNO";
    case CMD_ATUALIZAR_BLOCO:
        return "ATUALIZAR_BLOCO";
    case CMD_INVALIDAR_BLOCO:
        return "INVALIDAR_BLOCO";
    default:
        return "COMANDO_INVALIDO";
    }
}

void enviar_msg_assincrona(int rank_destino, int comando, int id_bloco, int offset, int tam, char *dados)
{
    int s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0)
        return;
    struct sockaddr_in server;
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons(BASE_PORT + rank_destino);
    if (connect(s, (struct sockaddr *)&server, sizeof(server)) >= 0)
    {
        uint32_t comando_net = htonl(comando);
        send(s, &comando_net, sizeof(uint32_t), 0);
        if (comando == CMD_ATUALIZAR_BLOCO)
        {
            uint32_t id_bloco_net = htonl(id_bloco);
            uint32_t offset_net = htonl(offset);
            uint32_t tam_net = htonl(tam);
            send(s, &id_bloco_net, sizeof(uint32_t), 0);
            send(s, &offset_net, sizeof(uint32_t), 0);
            send(s, &tam_net, sizeof(uint32_t), 0);
            send(s, dados, tam, 0);
        }
        else if (comando == CMD_INVALIDAR_BLOCO)
        {
            uint32_t id_bloco_net = htonl(id_bloco);
            send(s, &id_bloco_net, sizeof(uint32_t), 0);
        }
    }
    close(s);
}

void adicionar_bloco_na_cache(int id_bloco, char *dados_bloco)
{
    pthread_mutex_lock(&cache_mutex);
    int slot_vitima = proximo_slot_cache;
    printf("[P%d] [CACHE] Adicionando bloco %d no slot %d (substituindo bloco %d).\n",
           my_rank, id_bloco, slot_vitima, cache[slot_vitima].id);
    cache[slot_vitima].id = id_bloco;
    memcpy(cache[slot_vitima].dados, dados_bloco, T_BLOCO);
    cache[slot_vitima].valido = 1;
    proximo_slot_cache = (proximo_slot_cache + 1) % tamanho_cache;
    pthread_mutex_unlock(&cache_mutex);
}

int obter_bloco_remoto(int id_bloco, char *buffer_retorno)
{
    int dono = calcular_dono(id_bloco);
    if (dono < 0)
        return -1;
    int s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0)
        return -1;
    struct sockaddr_in server;
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons(BASE_PORT + dono);

    printf("[P%d] [REDE] Conectando ao P%d para obter o bloco %d...\n", my_rank, dono, id_bloco);
    if (connect(s, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        close(s);
        return -1;
    }

    uint32_t comando_net = htonl(CMD_OBTER_BLOCO_INTERNO);
    uint32_t id_bloco_net = htonl(id_bloco);
    send(s, &comando_net, sizeof(uint32_t), 0);
    send(s, &id_bloco_net, sizeof(uint32_t), 0);

    int recv_size = recv_all(s, buffer_retorno, T_BLOCO);
    close(s);

    if (recv_size == T_BLOCO)
    {
        adicionar_bloco_na_cache(id_bloco, buffer_retorno);
        return 0;
    }
    return -1;
}

void *handle_connection(void *socket_desc)
{
    int sock = *(int *)socket_desc;
    free(socket_desc);

    uint32_t comando_net;
    if (recv_all(sock, (char *)&comando_net, sizeof(uint32_t)) < 0)
    {
        close(sock);
        return NULL;
    }
    int command = ntohl(comando_net);
    printf("\n[P%d] [REDE] Conexão recebida. Comando: %s (%d)\n", my_rank, traduzir_comando(command), command);

    switch (command)
    {
    case CMD_OBTER_DADOS:
    {
        uint32_t pos_net, tam_net;
        recv_all(sock, (char *)&pos_net, sizeof(uint32_t));
        recv_all(sock, (char *)&tam_net, sizeof(uint32_t));
        int pos = ntohl(pos_net);
        int tam = ntohl(tam_net);
        printf("[P%d] [OBTER_DADOS] Processando pedido para ler %d bytes da posição %d.\n", my_rank, tam, pos);

        if (pos < 0 || (pos + tam) > (K_BLOCOS * T_BLOCO) || tam <= 0)
        {
            printf("[P%d] [ERRO] Pedido de leitura fora dos limites da memória. Enviando código %d.\n", my_rank, ERRO_MEMORIA_INEXISTENTE);
            uint32_t codigo_erro_net = htonl(ERRO_MEMORIA_INEXISTENTE);
            send(sock, &codigo_erro_net, sizeof(uint32_t), 0);
        }
        else
        {
            char *resultado = malloc(tam);
            int bytes_coletados = 0;
            int falha_geral = 0;
            for (int p_atual = pos; p_atual < pos + tam;)
            {
                int id_bloco, offset;
                mapear_posicao_global(p_atual, &id_bloco, &offset);
                int dono = calcular_dono(id_bloco);
                char *fonte_dados = malloc(T_BLOCO);
                int sucesso_leitura = 0;
                if (dono == my_rank)
                {
                    for (int i = 0; i < num_blocos_locais; i++)
                    {
                        if (blocos_locais[i].id == id_bloco)
                        {
                            memcpy(fonte_dados, blocos_locais[i].dados, T_BLOCO);
                            sucesso_leitura = 1;
                            break;
                        }
                    }
                }
                else
                {
                    pthread_mutex_lock(&cache_mutex);
                    for (int i = 0; i < tamanho_cache; i++)
                    {
                        if (cache[i].id == id_bloco && cache[i].valido)
                        {
                            memcpy(fonte_dados, cache[i].dados, T_BLOCO);
                            sucesso_leitura = 1;
                            break;
                        }
                    }
                    pthread_mutex_unlock(&cache_mutex);
                    if (!sucesso_leitura)
                    {
                        if (obter_bloco_remoto(id_bloco, fonte_dados) == 0)
                            sucesso_leitura = 1;
                    }
                }
                if (sucesso_leitura)
                {
                    int bytes_a_ler = T_BLOCO - offset;
                    if (bytes_a_ler > (tam - bytes_coletados))
                        bytes_a_ler = tam - bytes_coletados;
                    memcpy(resultado + bytes_coletados, fonte_dados + offset, bytes_a_ler);
                    bytes_coletados += bytes_a_ler;
                    p_atual += bytes_a_ler;
                }
                else
                {
                    falha_geral = 1;
                    free(fonte_dados);
                    break;
                }
                free(fonte_dados);
            }
            if (falha_geral)
            {
                uint32_t codigo_erro_net = htonl(ERRO_FALHA_OBTER_BLOCO);
                send(sock, &codigo_erro_net, sizeof(uint32_t), 0);
            }
            else
            {
                uint32_t status_sucesso_net = htonl(SUCESSO);
                send(sock, &status_sucesso_net, sizeof(uint32_t), 0);
                send(sock, resultado, tam, 0);
            }
            free(resultado);
        }
        break;
    }
    case CMD_OBTER_BLOCO_INTERNO:
    {
        uint32_t id_bloco_net;
        recv_all(sock, (char *)&id_bloco_net, sizeof(uint32_t));
        int id_bloco = ntohl(id_bloco_net);
        for (int i = 0; i < num_blocos_locais; i++)
        {
            if (blocos_locais[i].id == id_bloco)
            {
                send(sock, blocos_locais[i].dados, T_BLOCO, 0);
                break;
            }
        }
        break;
    }
    case CMD_SALVAR_DADOS:
    {
        uint32_t pos_net, tam_net;
        recv_all(sock, (char *)&pos_net, sizeof(uint32_t));
        recv_all(sock, (char *)&tam_net, sizeof(uint32_t));
        int pos = ntohl(pos_net);
        int tam = ntohl(tam_net);
        if (pos < 0 || (pos + tam) > (K_BLOCOS * T_BLOCO) || tam <= 0)
        {
            uint32_t codigo_erro_net = htonl(ERRO_MEMORIA_INEXISTENTE);
            send(sock, &codigo_erro_net, sizeof(uint32_t), 0);
        }
        else
        {
            char *dados_a_salvar = malloc(tam);
            recv_all(sock, dados_a_salvar, tam);
            for (int i = 0; i < tam;)
            {
                int p_atual = pos + i;
                int id_bloco, offset;
                mapear_posicao_global(p_atual, &id_bloco, &offset);
                int dono = calcular_dono(id_bloco);
                int bytes_a_escrever = T_BLOCO - offset;
                if (bytes_a_escrever > (tam - i))
                    bytes_a_escrever = tam - i;
                enviar_msg_assincrona(dono, CMD_ATUALIZAR_BLOCO, id_bloco, offset, bytes_a_escrever, dados_a_salvar + i);
                i += bytes_a_escrever;
            }
            free(dados_a_salvar);
            uint32_t status_sucesso_net = htonl(SUCESSO);
            send(sock, &status_sucesso_net, sizeof(uint32_t), 0);
        }
        break;
    }
    case CMD_ATUALIZAR_BLOCO:
    {
        uint32_t id_bloco_net, offset_net, tam_net;
        recv_all(sock, (char *)&id_bloco_net, sizeof(uint32_t));
        recv_all(sock, (char *)&offset_net, sizeof(uint32_t));
        recv_all(sock, (char *)&tam_net, sizeof(uint32_t));
        int id_bloco = ntohl(id_bloco_net);
        int offset = ntohl(offset_net);
        int tam = ntohl(tam_net);
        char *dados_recebidos = malloc(tam);
        recv_all(sock, dados_recebidos, tam);
        for (int i = 0; i < num_blocos_locais; i++)
        {
            if (blocos_locais[i].id == id_bloco)
            {
                memcpy(blocos_locais[i].dados + offset, dados_recebidos, tam);
                printf("[P%d] Bloco LOCAL %d atualizado.\n", my_rank, id_bloco);
                for (int p = 0; p < N_PROCESSOS; p++)
                {
                    if (p != my_rank)
                        enviar_msg_assincrona(p, CMD_INVALIDAR_BLOCO, id_bloco, 0, 0, NULL);
                }
                break;
            }
        }
        free(dados_recebidos);
        break;
    }
    case CMD_INVALIDAR_BLOCO:
    {
        uint32_t id_bloco_net;
        recv_all(sock, (char *)&id_bloco_net, sizeof(uint32_t));
        int id_bloco = ntohl(id_bloco_net);
        pthread_mutex_lock(&cache_mutex);
        for (int i = 0; i < tamanho_cache; i++)
        {
            if (cache[i].id == id_bloco && cache[i].valido)
            {
                cache[i].valido = 0;
                printf("[P%d] Cache para o bloco %d (slot %d) INVALIDADA.\n", my_rank, id_bloco, i);
                break;
            }
        }
        pthread_mutex_unlock(&cache_mutex);
        break;
    }
    default:
    {
        uint32_t codigo_erro_net = htonl(ERRO_COMANDO_DESCONHECIDO);
        send(sock, &codigo_erro_net, sizeof(uint32_t), 0);
    }
    }
    close(sock);
    return NULL;
}

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        fprintf(stderr, "Uso: %s <num_processos> <num_blocos> <tamanho_bloco>\n", argv[0]);
        exit(1);
    }
    N_PROCESSOS = atoi(argv[1]);
    K_BLOCOS = atoi(argv[2]);
    T_BLOCO = atoi(argv[3]);
    if (N_PROCESSOS <= 0 || K_BLOCOS <= 0 || T_BLOCO <= 0)
    {
        fprintf(stderr, "Argumentos devem ser numeros positivos.\n");
        exit(1);
    }
    pid_t pids[N_PROCESSOS];
    for (int i = 0; i < N_PROCESSOS - 1; i++)
    {
        pids[i] = fork();
        if (pids[i] < 0)
            die("fork falhou");
        if (pids[i] == 0)
        {
            my_rank = i + 1;
            break;
        }
    }
    printf("[P%d] Iniciado. PID: %d\n", my_rank, getpid());
    int blocos_por_processo = K_BLOCOS / N_PROCESSOS;
    int blocos_inicio = my_rank * blocos_por_processo;
    int blocos_fim = (my_rank == N_PROCESSOS - 1) ? (K_BLOCOS - 1) : (blocos_inicio + blocos_por_processo - 1);
    num_blocos_locais = blocos_fim - blocos_inicio + 1;
    if (num_blocos_locais > 0)
    {
        blocos_locais = malloc(sizeof(BlocoMemoria) * num_blocos_locais);
        for (int i = 0; i < num_blocos_locais; i++)
        {
            blocos_locais[i].id = blocos_inicio + i;
            blocos_locais[i].dados = malloc(T_BLOCO);
            memset(blocos_locais[i].dados, '-', T_BLOCO);
        }
    }
    printf("[P%d] Responsavel pelos blocos de %d a %d.\n", my_rank, blocos_inicio, blocos_fim);
    tamanho_cache = (int)(K_BLOCOS * 0.20);
    if (tamanho_cache == 0 && K_BLOCOS > 0)
        tamanho_cache = 1;
    if (tamanho_cache > 0)
    {
        printf("[P%d] Tamanho da cache: %d blocos.\n", my_rank, tamanho_cache);
        cache = malloc(sizeof(BlocoCache) * tamanho_cache);
        for (int i = 0; i < tamanho_cache; i++)
        {
            cache[i].id = -1;
            cache[i].dados = malloc(T_BLOCO);
            cache[i].valido = 0;
        }
    }
    pthread_mutex_init(&cache_mutex, NULL);

    int listening_socket;
    struct sockaddr_in server;
    listening_socket = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    if (setsockopt(listening_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)))
        die("setsockopt falhou");
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(BASE_PORT + my_rank);
    if (bind(listening_socket, (struct sockaddr *)&server, sizeof(server)) < 0)
        die("bind falhou");
    listen(listening_socket, MAX_CONEXOES);
    printf("[P%d] Escutando na porta %d...\n", my_rank, BASE_PORT + my_rank);

    while (1)
    {
        int client_sock = accept(listening_socket, NULL, NULL);
        if (client_sock < 0)
            continue;
        pthread_t connection_thread;
        int *new_sock = malloc(sizeof(int));
        *new_sock = client_sock;
        if (pthread_create(&connection_thread, NULL, handle_connection, (void *)new_sock) < 0)
        {
            perror("nao foi possivel criar a thread");
        }
    }
    return 0;
}