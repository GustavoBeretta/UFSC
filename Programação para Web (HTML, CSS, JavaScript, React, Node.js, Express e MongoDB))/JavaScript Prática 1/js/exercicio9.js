function haOnzeDigitos(cpf) {
    let n = cpf.length
    return n == 11
}

function todosOsOnzeDigitosSaoNumeros(cpf) {
    let list = cpf.split("")
    for (i = 0; i < cpf.length; i++) {
        if (isNaN(list[i])) {
            return false
        }
    }
    return true
}

function osOnzeNumerosSaoDiferentes(cpf) {
    let list = cpf.split("")
    for (i = 1; i < cpf.length; i++) {
        if (list[i] != list[i-1]){
            return true
        }
    }
    return false
}

function oPrimeiroDigitoVerificadorEhValido(cpf) {
    let list = cpf.split("")
    let soma = 0
    let n = 10
    for (let i = 0; i < 9; i++) {
        soma += Number(list[i])*n
        n -= 1
    }
    let resto = (soma * 10) % 11
    if (resto == 10) {
        resto = 0
    }
    if (resto == list[9]) {
        return true
    }
    return false
}

function oSegundoDigitoVerificadorEhValido(cpf) {
    let list = cpf.split("")
    let soma = 0
    let n = 11
    for (let i = 0; i < 10; i++) {
        soma += Number(list[i])*n
        n -= 1
    }
    let resto = (soma * 10) % 11
    if (resto == 10) {
        resto = 0
    }
    if (resto == list[10]) {
        return true
    }
    return false
}





//------------------- Não edite abaixo ----------------------------
function validarCPF(validacao, cpf) {
    switch (validacao) {
        case "onzeDigitos": return haOnzeDigitos(cpf)
        case "onzeSaoNumeros": return todosOsOnzeDigitosSaoNumeros(cpf) && validarCPF("onzeDigitos", cpf)
        case "naoSaoTodosIguais": return osOnzeNumerosSaoDiferentes(cpf) && validarCPF("onzeSaoNumeros", cpf)
        case "verificador10": return oPrimeiroDigitoVerificadorEhValido(cpf) && validarCPF("naoSaoTodosIguais", cpf)
        case "verificador11": return oSegundoDigitoVerificadorEhValido(cpf) && validarCPF("verificador10", cpf)

        default:
            console.error(validacao+" é um botão desconhecido...")
            return false
    }
}


function tratadorDeCliqueExercicio9(nomeDoBotao) {
    const cpf = document.getElementById("textCPF").value

    const validacao = (nomeDoBotao === "validade") ? "verificador11": nomeDoBotao
    const valido = validarCPF(validacao, cpf)
    const validoString = valido ? "valido": "inválido"
    const validadeMensagem = "O CPF informado ("+cpf+") é "+ validoString
    console.log(validadeMensagem)

    if (nomeDoBotao !== "validade") {
        let divResultado = document.getElementById(validacao);
        divResultado.textContent = validoString
        divResultado.setAttribute("class", valido ? "divValidadeValido": "divValidadeInvalido")    
    } else {
        window.alert(validadeMensagem)
    }

    
}