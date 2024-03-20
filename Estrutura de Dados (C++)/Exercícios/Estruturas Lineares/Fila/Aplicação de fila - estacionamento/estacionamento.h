// Copyright [2023] <GUSTAVO BERETTA GONÇALVES>

/*
    *** Importante ***

    O código de fila em vetor está disponível internamente (não precisa de implementação aqui)

*/



void retira_veiculo(structures::ArrayQueue<int> *f, int k) {
    for (int i = 0; i < k - 1; i++) {
        int carro = f[0].dequeue();
        f[0].enqueue(carro);
    }
    f[0].dequeue();
}


void mantenha_veiculo(structures::ArrayQueue<int> *f, int k) {
    int tam = f[0].size();
    for (int i = 0; i <= tam-1; i++) {
        int carro = f[0].dequeue();
        if (i == k-1) {
            f[0].enqueue(carro);
        }
    }
}



/*
    *** Importante ***

    A função 'main()' não deve ser escrita aqui, pois é parte do código dos testes e já está implementada

*/
