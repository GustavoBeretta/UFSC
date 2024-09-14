function Exercicio4() {

    let n1 = Number(window.prompt("Digite o primeiro número:"))
    console.log(typeof(n1))
    if (30 <= n1 && n1 <= 50) {
        console.log(`O número ${n1} está presente no intervalo [30, 50]`)
    } else if (60 <= n1 && n1 <= 100) {
        console.log(`O número ${n1} está presente no intervalo [60, 100]`)
    } else {
        console.log(`O número informado não está presente em nenhum intervalo`)
    }

    let n2 = Number(window.prompt("Digite o segundo número:"))
    if (30 <= n2 && n2 <= 50) {
        console.log(`O número ${n2} está presente no intervalo [30, 50]`)
    } else if (60 <= n2 && n2 <= 100) {
        console.log(`O número ${n2} está presente no intervalo [60, 100]`)
    } else {
        console.log(`O número informado não está presente em nenhum intervalo`)
    }

}