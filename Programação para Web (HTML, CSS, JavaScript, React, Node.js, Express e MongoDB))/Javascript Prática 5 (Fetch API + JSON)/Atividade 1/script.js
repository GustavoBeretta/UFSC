async function carregaufs() {
    try {
        const response = await fetch('https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome')
        const ufs = await response.json()
        for (let i = 0; i < ufs.length; i++) {
            const option = document.createElement('option')
            option.value = ufs[i].sigla
            option.textContent = ufs[i].nome;
            document.getElementById('ufs').appendChild(option)
        }
        document.getElementById('ufs').addEventListener('change', carregacidades())
    } catch(error) {
        window.alert(`Erro ao carregar as UFs: ${error}`)
    }
}

async function carregacidades() {
    document.getElementById('cidades').innerHTML=''
    const selecteduf = document.getElementById('ufs').value
    try {
        const response = await fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${selecteduf}/municipios?orderBy=nome`)
        const cidades = await response.json()
        for (let i = 0; i < cidades.length; i++) {
            const option = document.createElement('option')
            option.value = cidades[i].nome
            option.textContent = cidades[i].nome
            document.getElementById('cidades').appendChild(option)
        }
        document.getElementById('cidades').disabled = false
    } catch(error) {
        window.alert(`Erro ao carregar as cidades: ${error}`)
    }
}

carregaufs()