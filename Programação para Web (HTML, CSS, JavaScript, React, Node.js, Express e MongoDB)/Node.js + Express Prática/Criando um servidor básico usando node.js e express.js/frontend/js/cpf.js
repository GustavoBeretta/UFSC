class Cpf {
	constructor(value) {
		this._checkValidity(value)
		this._value = value
	}


	get value() {
		return this._value
	}


	_computeValidationDigit(value, size) {
		//para o primeiro dígito, size=9
		//para o segundo dígito, size=10

		//exemplo de value: "12345678910"
		const firstDigits = value.substring(0,size)
		//para primeiro dígito, firstDigits = "123456789"
		//para segundo dígito, firstDigits = "1234567891"
		const firstDigitsAsList = firstDigits.split("")
		//["1","2","3","4","5","6","7","8","9"]
		//["1","2","3","4","5","6","7","8","9","1"]
		let sum = 0
		for (var i = 0; i < firstDigitsAsList.length; i++) {
			sum+=(size-i+1)*firstDigitsAsList[i]
		} 
		sum*=10 //sum = sum * 10
		let resto = sum % 11
		if (resto == 10) {
			resto=0
		}
		return resto
	}


	_computeFirstValidationDigit(value) {
		return this._computeValidationDigit(value, 9)
	}


	_computeSecondValidationDigit(value) {
		return this._computeValidationDigit(value, 10)
	}


	_checkValidationDigits(value) {
		if (this._computeFirstValidationDigit(value) != value[9]) {
			throw new Error("Erro no primeiro dígito de verificação")
		}

		if (this._computeSecondValidationDigit(value) != value[10]) {
			throw new Error("Erro no segundo dígito de verificação")
		}
	}


	_allDigitsAreNumbers(value) {
		if (!value.match(/^[0-9]+$/)) {
			throw new Error("Todos os dígitos do CPF devem ser números!")
		}
	}


	_hasElevenDigits(value) {
		if (value.length != 11) {
			throw new Error(`CPF precisa ter 11 dígitos. Porém, ${value.length} informados.`);
		}
	}


	_allDigitsAreNotTheSame(value) {
		let valueAsList = value.split("")
		for (var i = 1; i < valueAsList.length; i++) {
			if (valueAsList[i] != valueAsList[i-1]) {
				return;
			}
		}
		throw new Error("Todos os dígitos do CPF informado são iguais!");
	}


	_checkValidity(value) {
		this._hasElevenDigits(value)//a
		this._allDigitsAreNumbers(value)//b		
		this._allDigitsAreNotTheSame(value)//c
		this._checkValidationDigits(value)//d, e
	}

	obterRegiaoFiscal() {
		let nonoDigito = this._value.substring(8, 9)
		switch (nonoDigito) {
			case "1": return "DF, GO, MT, MS e TO"
			case "2": return "AC, AP, AM, PA, RO e RR"
			case "3": return "CE, MA e PI"
			case "4": return "AL, PB, PE e RN"
			case "5": return "BA e SE"
			case "6": return "MG"
			case "7": return "ES e RJ"
			case "8": return "SP"
			case "9": return "PR e SC"
			case "0": return "RS"
			default: throw `Região fiscal ${nonoDigito} desconhecida`
		}
	}
}