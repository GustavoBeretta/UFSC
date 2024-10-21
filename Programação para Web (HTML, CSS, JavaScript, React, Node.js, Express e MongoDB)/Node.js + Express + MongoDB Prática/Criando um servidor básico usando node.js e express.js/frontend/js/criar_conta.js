let permitirCadastroSemValidacaoDosCampos = false;

let campoNomeUsuario = document.getElementById("cadastro-usuario")
let campoNome = document.getElementById("cadastro-nome")
let campoSobrenome = document.getElementById("cadastro-sobrenome")
let campoCPF = document.getElementById("cadastro-cpf")
let campoEmail = document.getElementById("cadastro-email")
let campoSenha = document.getElementById("cadastro-senha")
let campoRepitaSenha = document.getElementById("cadastro-repitaSenha")
let campoCEP = document.getElementById("cadastro-cep")
let campoLogradouro = document.getElementById("cadastro-logradouro")
let campoNumero = document.getElementById("cadastro-numero")
let campoComplemento = document.getElementById("cadastro-complemento")
let campoBairro = document.getElementById("cadastro-bairro")
let campoCidade = document.getElementById("cadastro-localidade")
let campoUF = document.getElementById("cadastro-uf")

let botaoCadastrar = document.getElementById("cadastro-botao")



function showErrorOnStatusElement(statusElement, text) {
    statusElement.classList.remove("material-icons")
    statusElement.classList.remove("status-ok")
    statusElement.classList.add("status-fail")
    statusElement.setAttribute("style", "")
    statusElement.textContent = text
}

function markStatusAsOk(statusElement) {
    statusElement.classList.add("material-icons")
    statusElement.classList.remove("status-fail")
    statusElement.classList.add("status-ok")
    statusElement.setAttribute("style", "font-size:18px;")
    statusElement.textContent = "check_circle"
}

function validaTextoEmBranco(textItem, statusItemId, nomeCampo) {
    const texto=textItem.value
    const status=document.getElementById(statusItemId)
    if (texto === "") {
        showErrorOnStatusElement(status, nomeCampo+" não pode estar em branco")
        return false
    } else {
        markStatusAsOk(status)
        return true
    }
}

function validaEmail(textItem, statusItemId, nomeCampo) {
    //https://stackoverflow.com/questions/46155/how-can-i-validate-an-email-address-in-javascript
    const func = (email) => {
        return String(email)
          .toLowerCase()
          .match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          );
      };
    const texto=textItem.value
    const status=document.getElementById(statusItemId)
    if (func(texto)) {
        markStatusAsOk(status)
        return true
    } else {
        showErrorOnStatusElement(status, nomeCampo+" inválido.")
        return false
    }
}

const temSimbolosEspeciais = (texto) => texto.match(/([!,%,&,@,#,$,^,*,?,_,~])/)
const temNumeros = (texto) => texto.match(/([0-9])/)
const temMaiusculasEMinusculas  = (texto) => texto.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)


function validaSenha(textItem, statusItemId, nomeCampo) {
    //solução adaptada de https://codepen.io/coding_beast/pen/LYGrXde
    const texto=textItem.value
    const status=document.getElementById(statusItemId)
    let passwordStrength = document.getElementById("password-strength")

    numeroDeCaracteres = texto.length
    if (numeroDeCaracteres == 0) {
        passwordStrength.style = 'width: 0%';
        showErrorOnStatusElement(status, nomeCampo+" não pode estar vazia.")
        return false
    }

    let forcaSenha = 0
    //ter símbolos especiais [!,%,&,@,#,$,^,*,?,_,~]
    let textoStatus = "Dicas para melhorar a força da senha: "
    if (temSimbolosEspeciais(texto)) {
        forcaSenha+=1;
    } else {
        textoStatus+="Inclua símbolos especiais (!,%,&,@,#,$,^,*,?,_,~). "
    }
    //ter números
    if (temNumeros(texto)) {
        forcaSenha+=1
    } else {
        textoStatus+="Inclua números. "
    }
    //mix de maiúsculos e minúsculos
    if (temMaiusculasEMinusculas(texto)) {
        forcaSenha+=1
    } else {
        textoStatus+="Misture letras maiúsculas e minúsculas. "
    }
    //ter ao menos 10 caracteres 0.1/caractere no máximo 1
    if(numeroDeCaracteres < 10) {
        forcaSenha+=numeroDeCaracteres*0.1
        textoStatus+=`Inclua ao menos 10 caracteres. Atualmente com ${numeroDeCaracteres}`
    } else {
        forcaSenha+=1
    } 
    
    let width=25*forcaSenha
    passwordStrength.style = `width: ${width}%`;
    passwordStrength.classList.remove('progress-bar-warning');
    passwordStrength.classList.remove('progress-bar-success');
    passwordStrength.classList.add('progress-bar-danger');
    if (width > 50) {
        passwordStrength.classList.remove('progress-bar-success');
        passwordStrength.classList.remove('progress-bar-danger');
        passwordStrength.classList.add('progress-bar-warning');
    } 
    if (width > 99) {
        passwordStrength.classList.remove('progress-bar-warning');
        passwordStrength.classList.remove('progress-bar-danger');
        passwordStrength.classList.add('progress-bar-success');
        markStatusAsOk(status)
        return true
    } else {
        showErrorOnStatusElement(status, textoStatus)
        return false
    }

}


function validaRepeticaoSenha(textItem, statusItemId) {
    let senha = document.getElementById("cadastro-senha").value
    const texto=textItem.value
    const status=document.getElementById(statusItemId)
    if (senha.length == 0) {
        showErrorOnStatusElement(status, "Senha vazia")
        return false
    }
    if (texto === senha) {
        markStatusAsOk(status)
        return true
    } else {
        showErrorOnStatusElement(status, "A senha não é igual!")
        return false
    }
}

function validarCPF(elementoCPF) {
    const status=document.getElementById("statusCPF")
    try {
        let cpf = new Cpf(elementoCPF.value)
        console.log(cpf)
        markStatusAsOk(status)
    } catch (error) {
        showErrorOnStatusElement(status, error.message)
        return false
    }
    return true
}

function validaCEP(campoCEP) {
    const cep = campoCEP.value.replace("-","")
    if (cep.length == 8)
        return true
    return false
}

async function validaNomeDoUsuario(campoNomeUsuario) {
    const options = {
        method: 'POST',
        mode: 'cors',
        cache: 'default',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username: campoNomeUsuario.value})
    }

    const result = await fetch("http://127.0.0.1:3125/api/check-user", options);
    const serverResponse = await result.json();
    const statusUsername = document.getElementById("statusUsername");
    if (serverResponse.userExists) {

        showErrorOnStatusElement(statusUsername, "O usuário informado já existe.");
        return false; //campo não foi validado com sucesso pois o usuário já existe
    }
    if (validaTextoEmBranco(campoNomeUsuario, "statusUsername", "Nome de usuário")) {
        markStatusAsOk(statusUsername);
        return true;
    }
    return false;
}

function validaNomeDeUsuarioEnquantoDigita(campoNomeDoUsuario, nomeStatus) {
    //esta função vai ser executada para cada keyup, logo não vamos fazer chamadas para o servidor a cada vez.
    //nesta validação mais simples vamos apenas verificar se o campo está vazio
    const status = document.getElementById("statusUsername")
    if (campoNomeDoUsuario.value === "") {
        showErrorOnStatusElement(status, nomeCampo+" não pode estar em branco")
    } else {
        //não usaremos o markStatusAsOk(status) aqui pois este campo deve ser verificado após ocorrer o evento blur
        showErrorOnStatusElement(status, "")
    }
}

async function validaFormularioCompleto() {

    let resultadoValidacao = []
    resultadoValidacao.push(validaTextoEmBranco(campoNome, 'statusNome', 'Nome'))
    resultadoValidacao.push(validaTextoEmBranco(campoSobrenome, 'statusSobrenome', 'Sobrenome'))
    resultadoValidacao.push(validarCPF(campoCPF))
    resultadoValidacao.push(validaEmail(campoEmail, 'statusEmail', 'E-mail'))
    resultadoValidacao.push(validaSenha(campoSenha, 'statusSenha', 'Senha'))
    resultadoValidacao.push(validaRepeticaoSenha(campoRepitaSenha, 'statusRepitaSenha'))
    resultadoValidacao.push(validaCEP(campoCEP))
    
    
    
    const usuarioValido = await validaNomeDoUsuario(campoNomeUsuario);
    console.log("Usuário válido: "+usuarioValido)
    resultadoValidacao.push(usuarioValido)

    const todosValidados = resultadoValidacao.reduce((p, e)=> p && e, true);
        
    if (permitirCadastroSemValidacaoDosCampos) {
        botaoCadastrar.disabled = false;
    } else {
        if (todosValidados) {
            console.log("Habilitando")
            botaoCadastrar.disabled = false;
        } else {
            console.log("desabiliando")
            botaoCadastrar.disabled = true;
        }
    }

}


campoNomeUsuario.addEventListener("blur", validaFormularioCompleto)
campoNome.addEventListener("blur", validaFormularioCompleto)
campoSobrenome.addEventListener("blur", validaFormularioCompleto)
campoCPF.addEventListener("blur", validaFormularioCompleto)
campoEmail.addEventListener("blur", validaFormularioCompleto)
campoSenha.addEventListener("blur", validaFormularioCompleto)
campoRepitaSenha.addEventListener("blur", validaFormularioCompleto)
campoCEP.addEventListener("blur", validaFormularioCompleto)

async function criarConta() {
    const options = {
        method: 'POST',
        mode: 'cors',
        cache: 'default',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"username": campoNomeUsuario.value, "nome": campoNome.value, "sobrenome": campoSobrenome.value, "email": campoEmail.value, "senha": campoSenha.value, "cep": campoCEP.value})
    }

    try {
        const response = await fetch('http://127.0.0.1:3125/api/create-user', options);
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Erro ao criar conta:', errorData.message);
            return;
        }

        const data = await response.json();
        console.log('Conta criada com sucesso:', data.message);

        limparFormulario();
    } catch (error) {
        console.error('Erro na requisição:', error);
    }
}

function limparFormulario() {
    campoNomeUsuario.value = "";
    campoNome.value = "";
    campoSobrenome.value = "";
    campoCPF.value = "";
    campoEmail.value = "";
    campoSenha.value = "";
    campoRepitaSenha.value = "";
    campoCEP.value = "";
    campoLogradouro.value = "";
    campoNumero.value = "";
    campoComplemento.value = "";
    campoBairro.value = "";
    campoCidade.value = "";
    campoUF.value = "";

    const statusElements = document.querySelectorAll(".status-fail, .status-ok");
    statusElements.forEach(element => {
        element.textContent = "";
        element.classList.remove("status-fail", "status-ok", "material-icons");
        element.setAttribute("style", "");
    });

    let passwordStrength = document.getElementById("password-strength");
    passwordStrength.style = "width: 0%;";
    passwordStrength.className = "progress-bar";

    botaoCadastrar.disabled = true;
}