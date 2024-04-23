function obterRegiaoFiscalAtravesDoCPFInformado(cpfInformado) {
    let list = cpfInformado.split("")
    let regiaoFiscal = list[8]
    return regiaoFiscal
}



function tratadorDeCliqueExercicio8() {
    let textCPF = document.getElementById("textCPF")
	let textRegiao = document.getElementById("regiaoFiscal")

    const regiaoFiscal = obterRegiaoFiscalAtravesDoCPFInformado(textCPF.value);
    textRegiao.textContent = "Região fiscal: "+regiaoFiscal
}
