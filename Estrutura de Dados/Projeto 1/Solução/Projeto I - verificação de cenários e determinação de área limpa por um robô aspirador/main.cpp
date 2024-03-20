// Copyright 2023 <Gustavo Beretta Gonçalves>

#include <iostream>
#include <string>
#include "array_stack.h"
#include <fstream>
#include "array_queue.h"
#include <algorithm>
#include <sstream>

// funcao de validacao das tags do arquivo
bool validacao(std::string nome_do_arquivo) {
    
    structures::ArrayStack<std::string> pilha_de_tags(20);
    
    std::ifstream arquivo;
    arquivo.open(nome_do_arquivo);
    
    // variavel que armazena o caractere sendo lido atualmente
    char caractere_atual;
    // variavel que identifica se o loop está rodando dentro do identificador da tag
    bool lendo_tag = false;
    // varaivel que identifica se a tag sendo lida é de fechamento
    bool tag_de_fechamento = false;
    // variavel que armazena o identificador da tag sendo lida
    std::string identificador = "";
    
    if (arquivo.is_open()) {
        while (!arquivo.eof()) {
            
            // atribui o caractere atual a uma variavel
            arquivo >> caractere_atual;
            
            // verifica se uma tag está terminando de ser declarada
            if (caractere_atual == '>') {
                
                // verifica se é uma tag de fechamento
                if (tag_de_fechamento) {
                    
                    // verifica se a pilha está vazia
                    if (pilha_de_tags.empty()) {
                        return false;
                    
                    // caso negativo, verifica se o topo da pilha é igual ao identificador lido
                    } else if (pilha_de_tags.top() == identificador) {
                        pilha_de_tags.pop();
                        tag_de_fechamento = false;
                        lendo_tag = false;
                        identificador = "";
                        caractere_atual = ' ';
                    
                    // caso negativo, retorna o erro
                    } else {
                        return false;
                    }
                    
                // caso negativo, empilha o identificador da tag lida    
                } else {
                    pilha_de_tags.push(identificador);
                    lendo_tag = false;
                    identificador = "";
                    caractere_atual = ' ';
                }
       
            }
            
            // verifica se uma tag está sendo lida    
            if (lendo_tag) {
                // verifica se é o símbolo de tag de fechamento
                if (caractere_atual == '/') {
                    tag_de_fechamento = true;
                // caso negativo, adiciona o caractere ao identificador
                } else {
                    identificador += caractere_atual; 
                }
            }
            
            // verifica se uma tag está sendo declarada
            if (caractere_atual == '<') {
                lendo_tag = true;
            }
        
        }
        
        // verifica se há tags que não foram fechadas
        if (pilha_de_tags.empty()) {
            return true;
        } else {
            return false;
        }
            
    }
    
    // retorna falso caso não consiga ler o arquivo
    return false;
}

// Função que retorna uma informação desejada do arquivo
std::string retorna_info(const std::string& string_conteudo, std::size_t pos_cenario, const std::string& tag, const std::string& var) {
    std::string dado;
    size_t startPos = string_conteudo.find("<" + tag + ">", pos_cenario);
    if (startPos != std::string::npos) {
        startPos = string_conteudo.find("<" + var + ">", startPos);
        if (startPos != std::string::npos) {
            size_t endPos = string_conteudo.find("</" + var + ">", startPos);
            if (endPos != std::string::npos){
                startPos += var.length() + 2;
                dado = string_conteudo.substr(startPos, endPos - startPos);
            }
        }
    }
    return dado;
}

// Função geradora de matrizes
int** gerador_matriz(const std::string& matriz_string, int altura, int largura, bool zerada) {
    int** matriz = new int*[altura];
    std::string matriz_valores = matriz_string;
    
    //Remove as quebras de linha
    matriz_valores.erase(std::remove(matriz_valores.begin(), matriz_valores.end(), '\n'), matriz_valores.end());

    // Atribuição de valores à matriz
    for (int i = 0; i < altura; i++) {
        matriz[i] = new int[largura];
        for (int j = 0; j < largura; j++) {
            char valor = matriz_valores[i * largura + j];
            // Matriz zerada ou não
            matriz[i][j] = zerada ? 0 : valor - '0';
        }
    }
    
    return matriz;
}

struct Coordenada {
    int x;
    int y;
};

//funcao que resolve o cenário
int resolucao(int** matriz_cenario, int** matriz_zerada, int altura, int largura, int x_robo, int y_robo) {
   
    int resultado = 0;
    Coordenada coord{x_robo, y_robo};
    structures::ArrayQueue<Coordenada> fila(100);

    // Posiciona o robo corretamente na matriz zerada; 
    if (matriz_cenario[x_robo][y_robo] == 1) {
        matriz_zerada[x_robo][y_robo] = 1;
        matriz_cenario[x_robo][y_robo] = 0;
        fila.enqueue(coord);
    } else {
        matriz_zerada[x_robo][y_robo] = 0;
    }


    while(!fila.empty()) {

        // Armazena o valor da primeira coordenada da fila em uma variável;
        Coordenada first = fila.dequeue();

        // vizinhança-4 da primeira coordenada da fila;
        Coordenada coordRight{first.x + 1, first.y};;
        Coordenada coordLeft{first.x - 1, first.y};
        Coordenada coordUp{first.x, first.y + 1};
        Coordenada coordDown{first.x, first.y - 1};

        if (coordRight.x < altura && coordRight.y >= 0 && coordRight.y < largura) {
            if (matriz_cenario[coordRight.x][coordRight.y] == 1) {
                matriz_zerada[coordRight.x][coordRight.y] = 1;
                matriz_cenario[coordRight.x][coordRight.y] = 0;
                fila.enqueue(coordRight);
            }
        }

        if (coordLeft.x >= 0 && coordLeft.y >= 0 && coordLeft.y < largura) {
            if (matriz_cenario[coordLeft.x][coordLeft.y] == 1) {
                matriz_zerada[coordLeft.x][coordLeft.y] = 1;
                matriz_cenario[coordLeft.x][coordLeft.y] = 0;
                fila.enqueue(coordLeft);
            }
        }

        if (coordUp.x >= 0 && coordUp.x < altura && coordUp.y >= 0) {
            if (matriz_cenario[coordUp.x][coordUp.y] == 1) {
                matriz_zerada[coordUp.x][coordUp.y] = 1;
                matriz_cenario[coordUp.x][coordUp.y] = 0;
                fila.enqueue(coordUp);
            }
        }


        if (coordDown.x >= 0 && coordDown.x < altura && coordDown.y >= 0 && coordDown.y < largura) {
            if (matriz_cenario[coordDown.x][coordDown.y] == 1) {
                matriz_zerada[coordDown.x][coordDown.y] = 1;
                matriz_cenario[coordDown.x][coordDown.y] = 0;
                fila.enqueue(coordDown);
            }
        }
    }

    for (int i = 0; i < altura; i++) {
        for (int j = 0; j < largura; j++) {
            if (matriz_zerada[i][j] == 1) {
                resultado++;
            }
        }
    }

    return resultado;
}

int main() {

    std::string xmlfilename;
    std::cin >> xmlfilename;  // entrada
   
    if (!validacao(xmlfilename)) {
        std::cout << "erro" << std::endl;
        return 1;
    }

    // Armazena o conteúdo do arquivo em uma variável do tipo string
    std::ifstream arquivo(xmlfilename);
    std::ostringstream conteudo_do_arquivo;
    conteudo_do_arquivo << arquivo.rdbuf();
    std::string string_conteudo = conteudo_do_arquivo.str();

    // Calcula a quantidade de cenários do arquivo
    int n_cenarios = 0;
    std::string tag = "<cenario>";
    std::size_t pos = 0;
    while ((pos = string_conteudo.find(tag, pos)) != std::string::npos) {
        n_cenarios++;
        pos += tag.length();
    }

    // Realiza as operações para resolver cada cenário
    std::size_t aux = 0;
    for (int i = 0; i < n_cenarios; i++) {
        
        //Armazena a posição inicial de cada cenário em uma variável
        std::size_t startPos = string_conteudo.find(tag, aux);

        // Coleta as informações necessárias para a resolução do cenário da vez
        std::string nome_cenario = retorna_info(string_conteudo, startPos, "cenario", "nome");
        int altura = std::stoi(retorna_info(string_conteudo, startPos,"dimensoes", "altura")); 
        int largura = std::stoi(retorna_info(string_conteudo, startPos,"dimensoes", "largura"));
        int x_robo = std::stoi(retorna_info(string_conteudo, startPos,"robo", "x"));
        int y_robo = std::stoi(retorna_info(string_conteudo, startPos,"robo", "y"));

        // Criação das matrizes necessárias para a resolução do cenário da vez
        std::string matriz_string = retorna_info(string_conteudo, startPos, "cenario", "matriz"); 
        int **matriz_cenario = gerador_matriz(matriz_string, altura, largura, false);
        int **matriz_zerada = gerador_matriz(matriz_string, altura, largura, true);

        // Com todas as informações adquiridas, chama a função que realiza a operação do robô
        int resultado = resolucao(matriz_cenario, matriz_zerada, altura, largura, x_robo, y_robo);

        // Imprime a solução do problema do desafio da vez
        std::cout << nome_cenario << " " << resultado << std::endl;

        // Atualiza o valor de aux para manter o correto funcionamento do loop
        std::size_t endPos = string_conteudo.find("</cenario>", aux);
        aux = endPos + 10;
        
    }

    return 0;
}
