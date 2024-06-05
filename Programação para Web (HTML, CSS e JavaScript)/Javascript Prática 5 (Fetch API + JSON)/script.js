async function carregaufs() {
    try {
        const response = await fetch('https://servicodados.ibge.gov.br/api/v1/localidades/estados')
        const ufs = await response.json()
        console.log(ufs)
    } catch(error) {
        window.alert(`Erro ao carregar as UFs: ${error}`)
    }

    console.log(typeof(ufs))
    ufs.forEach(uf => {
        const option = document.createElement('option');
        option.value = uf.sigla;
        option.textContent = uf.nome;
        ufSelect.appendChild(option);
    })

    /*console.log(ufs[0])

    for (let i = 0; i < ufs.length; i++) {
        const option = document.createElement('option')
        option.value = ufs[i].sigla
        option.textContent = ufs[i].nome;
        document.getElementById('ufs').appendChild(option)
    }*/
}

carregaufs()