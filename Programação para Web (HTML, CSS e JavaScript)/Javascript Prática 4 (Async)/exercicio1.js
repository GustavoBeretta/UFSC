const calculadora = (v1, v2, f) => f(v1,v2)

const soma = (v1, v2) => v1+v2

const subtrai = (v1, v2) => v1-v2

console.log(calculadora(31,12,soma))
console.log(calculadora(11,25,subtrai))