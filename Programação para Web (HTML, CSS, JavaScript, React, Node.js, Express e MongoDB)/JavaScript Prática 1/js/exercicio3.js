function Exercicio3() {
    
    let string = window.prompt('Escreva uma string:')
    let comp = string.length
    string = string.substring(1,comp-1)
    window.alert(string)
}