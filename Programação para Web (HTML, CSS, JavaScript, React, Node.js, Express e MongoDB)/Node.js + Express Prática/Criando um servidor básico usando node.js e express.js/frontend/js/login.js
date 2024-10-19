async function fazerLogin() {
    let campoEmail = document.getElementById("cadastro-email")
    let campoSenha = document.getElementById("cadastro-senha")

    const options = {
        method: 'POST',
        mode: 'cors',
        cache: 'default',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"email": campoEmail.value, "senha": campoSenha.value})
    }

    try {
        const response = await fetch('http://127.0.0.1:3125/login', options);
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Erro ao tentar fazer login:', errorData.message);
            return;
        }

        const data = await response.json();
        console.log(data.message);

    } catch (error) {
        console.error('Erro na requisição:', error);
    }
}