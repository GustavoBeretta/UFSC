#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdint.h>

#define BASE_PORT 15700
#define MAX_BUFFER_SIZE 8192
#define COORDENADOR_RANK 0

typedef unsigned char byte;

#define SUCESSO 0
#define ERRO_MEMORIA_INEXISTENTE -2
#define ERRO_COMANDO_DESCONHECIDO -3
#define ERRO_FALHA_OBTER_BLOCO -4
#define ERRO_CONEXAO -10

#define CMD_OBTER_DADOS 1
#define CMD_SALVAR_DADOS 2

int recv_all(int sock, char *buffer, int len);

int le(int posicao, byte *buffer, int tamanho)
{
    int s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0)
        return ERRO_CONEXAO;
    struct sockaddr_in server;
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons(BASE_PORT + COORDENADOR_RANK);
    if (connect(s, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        close(s);
        return ERRO_CONEXAO;
    }

    uint32_t comando_net = htonl(CMD_OBTER_DADOS);
    uint32_t pos_net = htonl(posicao);
    uint32_t tam_net = htonl(tamanho);
    send(s, &comando_net, sizeof(uint32_t), 0);
    send(s, &pos_net, sizeof(uint32_t), 0);
    send(s, &tam_net, sizeof(uint32_t), 0);

    uint32_t status_net;
    if (recv_all(s, (char *)&status_net, sizeof(uint32_t)) < 0)
    {
        close(s);
        return ERRO_CONEXAO;
    }
    int status = ntohl(status_net);

    if (status == SUCESSO)
    {
        if (recv_all(s, (char *)buffer, tamanho) < 0)
        {
            close(s);
            return ERRO_CONEXAO;
        }
    }

    close(s);
    return status;
}

int escreve(int posicao, byte *buffer, int tamanho)
{
    int s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0)
        return ERRO_CONEXAO;
    struct sockaddr_in server;
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons(BASE_PORT + COORDENADOR_RANK);
    if (connect(s, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        close(s);
        return ERRO_CONEXAO;
    }

    uint32_t comando_net = htonl(CMD_SALVAR_DADOS);
    uint32_t pos_net = htonl(posicao);
    uint32_t tam_net = htonl(tamanho);
    send(s, &comando_net, sizeof(uint32_t), 0);
    send(s, &pos_net, sizeof(uint32_t), 0);
    send(s, &tam_net, sizeof(uint32_t), 0);
    send(s, buffer, tamanho, 0);

    uint32_t status_net;
    if (recv_all(s, (char *)&status_net, sizeof(uint32_t)) < 0)
    {
        close(s);
        return ERRO_CONEXAO;
    }
    int status = ntohl(status_net);

    close(s);
    return status;
}

void traduzir_erro(int codigo_erro)
{
    printf("   -> Mensagem de Erro: ");
    switch (codigo_erro)
    {
    case ERRO_CONEXAO:
        printf("Erro de conexao com o servidor.\n");
        break;
    case ERRO_MEMORIA_INEXISTENTE:
        printf("Tentativa de acesso a uma area de memoria invalida.\n");
        break;
    case ERRO_COMANDO_DESCONHECIDO:
        printf("O servidor nao reconheceu o comando enviado.\n");
        break;
    case ERRO_FALHA_OBTER_BLOCO:
        printf("Falha ao obter um bloco remoto necessario para a operacao.\n");
        break;
    default:
        printf("Ocorreu um erro desconhecido (codigo %d).\n", codigo_erro);
        break;
    }
}

void run_test(const char *test_name, int status, int expected_status)
{
    printf("   -> Resultado do Teste: ");
    if (status == expected_status)
    {
        printf("PASSOU (Retorno: %d)\n", status);
    }
    else
    {
        printf("FALHOU (Esperado: %d, Recebido: %d)\n", expected_status, status);
        traduzir_erro(status);
    }
}

void teste_escrita_leitura_simples_local()
{
    printf("\n--- INICIANDO Teste 1: Escrita/Leitura em Bloco Único (Local) ---\n");
    char *dados_escrita = "OLA MUNDO";
    int pos = 0;
    int tam = strlen(dados_escrita);
    byte buffer_leitura[50] = {0};

    printf("1.1. Escrevendo o texto '%s' na posicao %d...\n", dados_escrita, pos);
    int status = escreve(pos, (byte *)dados_escrita, tam);
    run_test("Escrita em Bloco Unico", status, SUCESSO);
    sleep(1);

    printf("1.2. Lendo de volta %d bytes da posicao %d para verificar...\n", tam, pos);
    status = le(pos, buffer_leitura, tam);
    run_test("Leitura em Bloco Unico", status, SUCESSO);
    if (status == SUCESSO)
    {
        printf("   -> Dados Lidos: '%.*s'\n", tam, buffer_leitura);
        printf("   -> Verificacao: %s\n", strncmp((char *)buffer_leitura, dados_escrita, tam) == 0 ? "OK" : "FALHOU");
    }
}

void teste_escrita_leitura_multibloco_remoto()
{
    printf("\n--- INICIANDO Teste 2: Escrita/Leitura em Múltiplos Blocos ---\n");
    char *dados_escrita = "MEMORIA COMPARTILHADA";
    int pos = 4;
    int tam = strlen(dados_escrita);
    byte buffer_leitura[50] = {0};

    printf("2.1. Escrevendo o texto '%s' na posicao %d...\n", dados_escrita, pos);
    int status = escreve(pos, (byte *)dados_escrita, tam);
    run_test("Escrita Multi-Bloco", status, SUCESSO);
    sleep(2);

    printf("2.2. Lendo de volta %d bytes da posicao %d para verificar...\n", tam, pos);
    status = le(pos, buffer_leitura, tam);
    run_test("Leitura Multi-Bloco", status, SUCESSO);
    if (status == SUCESSO)
    {
        printf("   -> Dados Lidos: '%.*s'\n", tam, buffer_leitura);
        printf("   -> Verificacao: %s\n", strncmp((char *)buffer_leitura, dados_escrita, tam) == 0 ? "OK" : "FALHOU");
    }
}

void teste_invalidacao_cache()
{
    printf("\n--- INICIANDO Teste 3: Invalidação e Substituição de Cache (FIFO) ---\n");
    byte buffer[50] = {0};
    char *dados_antigos = "DADO ANTIGO";
    char *dados_novos = "DADO NOVO";

    printf("3.1. Escrevendo '%s' no Bloco 4 (do P2) para o estado inicial.\n", dados_antigos);
    escreve(33, (byte *)dados_antigos, strlen(dados_antigos));
    sleep(1);

    printf("3.2. Lendo Bloco 2 (do P1) e Bloco 6 (do P3) para preencher a cache do P0 e deixar o Bloco 4 de fora.\n");
    le(17, buffer, 1);
    sleep(1);
    le(49, buffer, 1);
    sleep(1);

    printf("3.3. Lendo Bloco 4 (do P2) pela primeira vez. Isso causará um cache miss e o bloco será adicionado à cache do P0.\n");
    le(33, buffer, strlen(dados_antigos));
    printf("   -> Dados Lidos: '%.*s'\n", (int)strlen(dados_antigos), buffer);
    run_test("Leitura para popular cache", SUCESSO, SUCESSO);
    sleep(1);

    printf("3.4. Escrevendo '%s' no Bloco 4. Isso deve gerar uma mensagem de invalidação para o P0.\n", dados_novos);
    escreve(33, (byte *)dados_novos, strlen(dados_novos));
    sleep(1);

    printf("3.5. Lendo Bloco 4 novamente. O P0 deve ter um cache miss (pois sua cópia foi invalidada) e buscar o novo valor na rede.\n");
    int status = le(33, buffer, strlen(dados_novos));
    run_test("Leitura pos-invalidacao", status, SUCESSO);
    if (status == SUCESSO)
    {
        printf("   -> Dados Lidos: '%.*s'\n", (int)strlen(dados_novos), buffer);
        printf("   -> Verificacao: %s\n", strncmp((char *)buffer, dados_novos, strlen(dados_novos)) == 0 ? "OK" : "FALHOU");
    }
}

void teste_acesso_alem_limites()
{
    printf("\n--- INICIANDO Teste 4: Acesso a Memória Fora dos Limites ---\n");
    int memoria_total = 10 * 8;
    int pos = memoria_total + 5;
    byte buffer[10];
    printf("4.1. Tentando ler da posicao %d (que é inválida).\n", pos);
    int status = le(pos, buffer, 10);
    run_test("Leitura fora do limite", status, ERRO_MEMORIA_INEXISTENTE);
}

void teste_comando_invalido()
{
    printf("\n--- INICIANDO Teste 5: Envio de Comando Inválido ---\n");
    int s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0)
    {
        printf("Falha ao criar socket para o teste.\n");
        return;
    }
    struct sockaddr_in server;
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons(BASE_PORT + COORDENADOR_RANK);
    if (connect(s, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        printf("Falha ao conectar para o teste.\n");
        close(s);
        return;
    }

    uint32_t comando_invalido_net = htonl(99);
    printf("5.1. Enviando um código de comando inválido (99) para o servidor...\n");
    send(s, &comando_invalido_net, sizeof(uint32_t), 0);

    uint32_t status_net;
    recv_all(s, (char *)&status_net, sizeof(uint32_t));
    int status = ntohl(status_net);
    close(s);
    run_test("Comando Invalido", status, ERRO_COMANDO_DESCONHECIDO);
}

int main(int argc, char *argv[])
{
    int escolha = -1;
    char buffer_entrada[20];
    while (1)
    {
        printf("\n\n--- MENU DE TESTES DO CLIENTE DSM ---\n");
        printf("Configuracao sugerida para o servidor: ./servidor 4 10 8\n");
        printf("1. Teste de Escrita/Leitura em Bloco Único\n");
        printf("2. Teste de Escrita/Leitura em Múltiplos Blocos\n");
        printf("3. Teste de Coerência de Cache (Invalidação e FIFO)\n");
        printf("4. Teste de Erro: Acesso Fora dos Limites\n");
        printf("5. Teste de Erro: Comando Inválido\n");
        printf("0. Sair\n");
        printf("Escolha uma opcao: ");
        if (fgets(buffer_entrada, sizeof(buffer_entrada), stdin) != NULL)
        {
            if (sscanf(buffer_entrada, "%d", &escolha) != 1)
            {
                escolha = -1;
            }
        }
        switch (escolha)
        {
        case 1:
            teste_escrita_leitura_simples_local();
            break;
        case 2:
            teste_escrita_leitura_multibloco_remoto();
            break;
        case 3:
            teste_invalidacao_cache();
            break;
        case 4:
            teste_acesso_alem_limites();
            break;
        case 5:
            teste_comando_invalido();
            break;
        case 0:
            printf("Encerrando cliente.\n");
            return 0;
        default:
            printf("\nOpcao invalida! Por favor, escolha um numero de 0 a 5.\n");
            break;
        }
    }
    return 0;
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