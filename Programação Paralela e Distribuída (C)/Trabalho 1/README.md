# Trabalho_01_Paralela
Código desenvolvido para trabalho 1 da matéria Programação Paralela e Distribuída


/*
 * Projeto: Sistema de Atendimento com Prioridade e Relatórios
 * Funcionalidades:
 *  - 100 clientes (preferenciais ou comuns)
 *  - 4 Threads (podem ser caixa ou consumidor)
 *  - Somente 2 Threads podem ser caixas
 *  - Prioridade de atendimento
 *  - Fila de tarefas de relatório com consumidor dormindo via pthread_cond_t
 *  - Consumidor gerando relatorio de atendimento
 *  - Uso de pthreads, mutex, semáforos, e condição
 */

Windows
1. Instalar MSYS2 e toolchain UCRT64
Baixe e instale o MSYS2: https://www.msys2.org/

Abra o terminal MSYS2 UCRT64 (procure por "MSYS2 UCRT64" no menu iniciar)

Atualize os pacotes:
pacman -Syu

Instale o toolchain completo para compilação:
pacman -S mingw-w64-ucrt-x86_64-toolchain
Obs: Caso encontre erros de download, tente trocar o mirror ou verificar a conexão.

2. Navegar até a pasta do projeto
No terminal MSYS2 UCRT64, digite:
cd nome-da-pasta-onde-baixou
Atenção: O caminho deve ser em formato Unix com /c/ para o drive C:.

3. Compilar o programa
Use o gcc do UCRT64 para compilar, incluindo a biblioteca de threads POSIX:

/ucrt64/bin/gcc -Wall -Wextra -g3 main.c -o main.exe -lpthread]

Se o gcc estiver no PATH, você pode apenas usar:
gcc -Wall -Wextra -g3 main.c -o main.exe -lpthread

4. Executar o programa
Ainda no terminal, execute:
./main.exe




Para usuários Linux
1. Instalar gcc e pthreads
No terminal, instale o gcc e as libs pthread:

Debian/Ubuntu
sudo apt-get update
sudo apt-get install build-essential

Fedora:
sudo dnf install gcc gcc-c++

2. Navegar até a pasta do projeto
cd /caminho/para/seu/projeto

3. Compilar o programa
gcc -Wall -Wextra -g3 main.c -o main.exe -lpthread

4. Executar o programa
./main.exe



Descrição do Projeto
Este projeto implementa uma aplicação concorrente simulando o atendimento de clientes em caixas, com prioridade para clientes preferenciais. A aplicação utiliza threads para realizar o atendimento e geração de relatórios simultaneamente, garantindo o controle de concorrência e sincronização através de diferentes estruturas.

Estruturas de Sincronização Utilizadas
Mutex (pthread_mutex_t): Protege o acesso às filas de clientes e de tarefas, evitando condições de corrida ao inserir ou remover elementos.

Semáforo (sem_t): Controla o número máximo de caixas ativos simultaneamente, limitando a concorrência a um valor definido.

Variável de condição (pthread_cond_t): Permite que as threads consumidoras esperem por tarefas de relatório a serem produzidas.

Padrões de Projeto Implementados
Produtor-Consumidor
O padrão Produtor-Consumidor é adotado para desacoplar o processo de atendimento (produção de tarefas de relatório) da gravação das informações nos arquivos (consumo das tarefas). As threads atuam como produtores quando atendem clientes e geram tarefas, e como consumidores quando processam e gravam relatórios dessas tarefas.

Thread Pool / Worker Threads
Um conjunto fixo de threads genéricas é criado no início da aplicação e reutilizado tanto para atendimento (caixas) quanto para consumo de tarefas. Isso evita overhead de criação e destruição frequente de threads, garantindo melhor desempenho e controle sobre o paralelismo.