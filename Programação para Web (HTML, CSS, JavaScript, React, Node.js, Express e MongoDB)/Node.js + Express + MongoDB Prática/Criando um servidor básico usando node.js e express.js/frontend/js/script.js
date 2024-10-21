function aplicarNaTela(tela, mostrar) {
    if (mostrar) {
        tela.classList.remove("oculto")
    } else {
        tela.classList.add("oculto")
    }
}

function aplicarNasQuatroTelas(home, login, conta, main) {
    aplicarNaTela(document.getElementById("login-body"), login)
    aplicarNaTela(document.getElementById("novaConta"), conta)
    aplicarNaTela(document.getElementById("divHome"), home)
    aplicarNaTela(document.getElementById("mainpage"), main)
}

function mostrarApenasHome() {
    aplicarNasQuatroTelas(true, false, false, false)
}

function mostrarApenasLogin() {
    aplicarNasQuatroTelas(false, true, false, false)
}

function mostrarApenasConta() {
    aplicarNasQuatroTelas(false, false, true, false)
}

function mostrarApenasMain() {
    aplicarNasQuatroTelas(false, false, false, true)
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