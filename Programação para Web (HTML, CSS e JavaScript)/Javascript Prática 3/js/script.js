function mostrarApenasHome() {
    document.getElementById('divHome').style.display = 'block'
    document.getElementById('login-body').style.display = 'none'
    document.getElementById('nova-conta').style.display = 'none'
}

function mostrarApenasLogin() {
    document.getElementById('divHome').style.display = 'none'
    document.getElementById('login-body').style.display = 'block'
    document.getElementById('nova-conta').style.display = 'none'
    document.getElementById('campo-email').value=''
    document.getElementById('login-password').value=''

}

function mostrarApenasConta() {
    document.getElementById('divHome').style.display = 'none'
    document.getElementById('login-body').style.display = 'none'
    document.getElementById('nova-conta').style.display = 'block'
    document.getElementById('nome').value=''
    document.getElementById('sobrenome').value=''
    document.getElementById('cpf').value=''
    document.getElementById('email').value=''
    document.getElementById('senha').value=''
    document.getElementById('senhaa').value=''
    document.getElementById('statusNome').style.display = 'none'
    document.getElementById('statusSobrenome').style.display = 'none'
    document.getElementById('statusCPF').style.display = 'none'
    document.getElementById('statusEmail').style.display = 'none'
    document.getElementById('statusSenha').style.display = 'none'
    document.getElementById('statusRepitaSenha').style.display = 'none'
}

function camposPreenchidos() {
    if (document.getElementById('login-password').value && document.getElementById('campo-email').value.split('@').length == 2) {
        document.getElementById('botaoLogin').disabled = false
    } else {
        document.getElementById('botaoLogin').disabled = true
    }
}

function checaTexto(id, status) {
    if (document.getElementById(id).value) {
        document.getElementById(status).innerText = '✅'
        return true
    } else {
        document.getElementById(status).innerText = 'Não validado: o campo deve conter pelo menos um caracter'
        return false
    }
}

class CPF{
    constructor(cpf){
        this.cpf = cpf
        if (!this.validarCPF()) {
            throw new Error('Não validado')
        }
    }

    haOnzeDigitos(cpf) {
        let n = cpf.length
        return n == 11
    }
    
    todosOsOnzeDigitosSaoNumeros(cpf) {
        let list = cpf.split("")
        for (let i = 0; i < cpf.length; i++) {
            if (isNaN(list[i])) {
                return false
            }
        }
        return true
    }
    
    osOnzeNumerosSaoDiferentes(cpf) {
        let list = cpf.split("")
        for (let i = 1; i < cpf.length; i++) {
            if (list[i] != list[i-1]){
                return true
            }
        }
        return false
    }
    
    oPrimeiroDigitoVerificadorEhValido(cpf) {
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
    
    oSegundoDigitoVerificadorEhValido(cpf) {
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

    validarCPF() {
        return (this.haOnzeDigitos(this.cpf) && this.todosOsOnzeDigitosSaoNumeros(this.cpf) && this.osOnzeNumerosSaoDiferentes(this.cpf) && this.oPrimeiroDigitoVerificadorEhValido(this.cpf) && this.oSegundoDigitoVerificadorEhValido(this.cpf))
    }
}

function checaCPF(){
    try {
        let cpf_object = new CPF(document.getElementById('cpf').value)
        document.getElementById('statusCPF').innerText = '✅'
        return true
    } catch(erro) {
        document.getElementById('statusCPF').innerText = erro.message
        return false
    }
}

function checaSenha() {
    if (document.getElementById('senhaa').value && document.getElementById('senhaa').value == document.getElementById('senha').value) {
        document.getElementById('statusRepitaSenha').innerText = '✅'
        return true
    } else {
        document.getElementById('statusRepitaSenha').innerText = 'Não validado: a senha deve conter pelo menos um caracter e ser igual a digitada anteriormente'
        return false
    }
}

function checaEmail() {
    if (document.getElementById('email').value.split('@').length == 2) {
        document.getElementById('statusEmail').innerText = '✅'
        return true
    } else {
        document.getElementById('statusEmail').innerText = 'Não validado: o email deve conter um e apenas um "@"'
        return false
    }
}

function validaCriacao(status_atual) {
    let nome = checaTexto("nome", "statusNome")
    let sobrenome = checaTexto("sobrenome", "statusSobrenome")
    let cpf = checaCPF()
    let email = checaEmail()
    let senha = checaTexto("senha", "statusSenha")
    let senhaa = checaSenha()
    if (nome && sobrenome && cpf && email && senha && senhaa) {
        document.getElementById('BotaoConta').disabled = false
    } else {
        document.getElementById('BotaoConta').disabled = true
    }
    document.getElementById(status_atual).style.display = 'block'
}

