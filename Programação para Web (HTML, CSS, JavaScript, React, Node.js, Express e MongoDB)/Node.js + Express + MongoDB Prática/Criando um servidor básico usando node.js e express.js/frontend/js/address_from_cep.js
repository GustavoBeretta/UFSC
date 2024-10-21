function getAddressFromCEP(cep) {
    const search = cep.replace("-","")
    const options = {
        method: 'GET',
        mode: 'cors',
        cache: 'default'
    }
    fetch(`https://viacep.com.br/ws/${search}/json/`, options)
        .then(onSuccessCEPConsult)
        .then(onSuccessCEPJson)
}

function onSuccessCEPConsult(result) {
    return result.json();
}

function onSuccessCEPJson(endereco) {
    document.getElementById("cadastro-logradouro").value=endereco.logradouro
    document.getElementById("cadastro-bairro").value=endereco.bairro
    document.getElementById("cadastro-localidade").value=endereco.localidade
    document.getElementById("cadastro-uf").value=endereco.uf
}