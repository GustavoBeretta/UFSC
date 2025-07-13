Projeto de Memória Compartilhada Distribuída
Nomes: Luiz Adriano, Andres Kindel e Gustavo Beretta Gonçalves

Este projeto implementa um protótipo de um sistema de Memória Compartilhada Distribuída (DSM) em C. O sistema utiliza múltiplos processos, criados com fork(), que se comunicam via Sockets TCP..

Pré-requisitos
Ambiente Unix-like (macOS ou Linux).

Compilador C (como gcc ou clang).

Compilação
Para compilar os programas, navegue até a pasta do projeto no seu terminal e execute os seguintes comandos:

Compilar o Servidor:
gcc servidor.c -o servidor -lpthread

Compilar o Cliente:
gcc cliente.c -o cliente

Execução
A execução do sistema requer dois terminais abertos simultaneamente na pasta do projeto.

Parâmetros do Servidor
O servidor deve ser iniciado com três parâmetros numéricos obrigatórios:

./servidor <num_processos> <num_blocos> <tamanho_bloco>
<num_processos>: O número total de processos que irão compor o sistema DSM.
<num_blocos>: O número total de blocos de memória no sistema.
<tamanho_bloco>: O tamanho de cada bloco, em bytes.

Para que os casos de teste pré-configurados no cliente funcionem corretamente, você deve iniciar o servidor com os seguintes parâmetros:
num_processos: 4
num_blocos: 10
tamanho_bloco: 8

Passo a Passo para Rodar(Servidor)
Abra o Terminal 1 e inicie o servidor com os parâmetros corretos:
./servidor 4 10 8
O terminal exibirá os logs de inicialização de cada processo e permanecerá ativo, escutando por conexões. Deixe esta janela aberta.

Abra o Terminal 2 e inicie o cliente:
./cliente
O menu interativo com a lista de testes disponíveis será exibido.
No menu do cliente, digite o número do teste que deseja executar e pressione Enter. Observe os logs tanto no terminal do cliente (para ver os resultados dos testes) quanto no terminal do servidor (para ver o fluxo de comunicação entre os processos).
