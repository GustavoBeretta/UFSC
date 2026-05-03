# Analisador Léxico e Sintático - Compiladores

Projeto desenvolvido para a disciplina de Introdução a Compiladores, implementando um analisador léxico e um sintático.

## Integrantes
- Gustavo Beretta Gonçalves
- Luana Ronau Mattos
- Rafaela Silva Borges

## Estrutura dos Arquivos
- **/lexico**
    - `analisador_lexico.py`: Implementação da Parte 1.
    - `sem_erro.lsi`: Código fonte válido contendo funções, condicionais e operações aritméticas para testar o sucesso da tokenização.
    - `com_erro.lsi`: Código fonte contendo caracteres inválidos (ex: '@') propositalmente inseridos para testar o disparo de erros léxicos.
- **/sintatico**
    - `analisador_sintatico.py`: Implementação da Parte 3.
    - `teste_sucesso.lsi`: Arquivo com >50 linhas para teste positivo.
    - `erro_sintatico_1.lsi`: Teste de falta de ponto e vírgula.
    - `erro_sintatico_2.lsi`: Teste de parênteses faltantes.
    - `erro_sintatico_3.lsi`: Teste de regra inválida (print sem argumento).

---

## Analisador léxico: Instruções de execução 

Para executar o analisador léxico, siga os passos abaixo:

### 1. Acesse a pasta do analisador léxico
Abra o terminal e navegue até o diretório onde está o arquivo:

`cd lexico`

### 2. Execute o analisador passando o arquivo de entrada
Já dentro da pasta, digitar o seguinte comando:

`python3 analisador_lexico.py sem_erro.lsi`

Ou, para testar o comportamento com erros léxicos:

`python3 analisador_lexico.py com_erro.lsi`

---

## Analisador sintático: Instruções de execução 

Para executar o analisador sintático, que chama o léxico automaticamente:

1. Abra o terminal na pasta do projeto:

`cd sintatico`

2. Já dentro da pasta, digitar o seguinte comando:

`python3 analisador_sintatico.py teste_sucesso.lsi`

Ou, para testar o comportamento com erros sintáticos:

`python3 analisador_sintatico.py erro_sintatico_1.lsi`

`python3 analisador_sintatico.py erro_sintatico_2.lsi`

`python3 analisador_sintatico.py erro_sintatico_3.lsi`
