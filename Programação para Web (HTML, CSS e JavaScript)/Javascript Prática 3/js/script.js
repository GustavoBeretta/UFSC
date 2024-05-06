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
}

function camposPreenchidos() {
    if (document.getElementById('login-password').value && document.getElementById('campo-email').value.split('@').length == 2) {
        document.getElementById('botaoLogin').style.display = 'block'
    } else {
        document.getElementById('botaoLogin').style.display = 'none'
    }
}

function validaTexto(id, status) {
    if (document.getElementById(id).value) {
        document.getElementById(status).style.backgroundColor = 'green'
        return true
    } else {
        document.getElementById(status).style.backgroundColor = 'red'
        return false
    }
}

function validaSenha() {
    if (document.getElementById('senhaa').value && document.getElementById('senhaa').value == document.getElementById('senha').value) {
        document.getElementById('statusRepitaSenha').style.backgroundColor = 'green'
        return true
    } else {
        document.getElementById('statusRepitaSenha').style.backgroundColor = 'red'
        return false
    }
}

function validaEmail() {
    if (document.getElementById('email').value.split('@').length == 2) {
        document.getElementById('statusEmail').style.backgroundColor = 'green'
        return true
    } else {
        document.getElementById('statusEmail').style.backgroundColor = 'red'
        return false
    }
}

class CPF{
    constructor(cpf){
        this.cpf = cpf
        if (!this.validarCPF()) {
            throw new Error('CPF inválido')
        }
    }

    validarCPF(){
        return this.cpf.length == 11
    }
}