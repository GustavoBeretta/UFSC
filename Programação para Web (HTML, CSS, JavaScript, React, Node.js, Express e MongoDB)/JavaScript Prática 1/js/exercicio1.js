//atualize esta função
function tratadorDeCliqueExercicio1() {

    let valorComoString = window.prompt("Insira um valor numérico: ")

    console.log("O valor informado é: "+valorComoString)
    console.log("O valor informado é do tipo: "+ typeof valorComoString)

    let valorComoInteiro = Number(valorComoString)

    console.log("O valor como inteiro é: "+valorComoInteiro)
    console.log("O valor como inteiro é do tipo: "+typeof valorComoInteiro)
}