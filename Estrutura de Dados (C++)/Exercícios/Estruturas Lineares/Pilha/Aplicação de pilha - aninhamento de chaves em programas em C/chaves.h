// Copyright [2022] <GUSTAVO BERETTA GONÇALVES >
#include <string>
#include "./array_stack.h"

bool verificaChaves(std::string trecho_programa) {
    bool resposta = true;
    int  tamanho  = trecho_programa.length();
    structures::ArrayStack<char> pilha(500);
    for (int i = 0; i < tamanho; i++) {
        if (trecho_programa[i] == '{') {
            pilha.push(trecho_programa[i]);
        } else if (trecho_programa[i] == '}') {
            if (pilha.empty()) {
                resposta = false;
            } else {
                pilha.pop();
            }
        }
    }
    if (pilha.empty()) {
        return resposta;
    } else {
        resposta = false;
        return resposta;
    }
}
