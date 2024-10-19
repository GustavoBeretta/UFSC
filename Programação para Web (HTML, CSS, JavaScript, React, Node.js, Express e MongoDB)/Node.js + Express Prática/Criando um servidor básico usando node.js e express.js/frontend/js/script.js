function aplicarNaTela(tela, mostrar) {
    if (mostrar) {
        tela.classList.remove("oculto")
    } else {
        tela.classList.add("oculto")
    }
}

function aplicarNasTrêsTelas(home, login, conta) {
    aplicarNaTela(document.getElementById("login-body"), login)
    aplicarNaTela(document.getElementById("novaConta"), conta)
    aplicarNaTela(document.getElementById("divHome"), home)
}

function mostrarApenasHome() {
    aplicarNasTrêsTelas(true, false, false)
}

function mostrarApenasLogin() {
    aplicarNasTrêsTelas(false, true, false)
}

function mostrarApenasConta() {
    aplicarNasTrêsTelas(false, false, true)
}

function mostrarTelaInicial() {
    switch (telaInicial) {
        case "Login": mostrarApenasLogin(); break;
        case "CriarConta": mostrarApenasConta(); break;
        case "Home":
        default: mostrarApenasHome()
    }
}

const telaInicial = "Login"
mostrarTelaInicial()