function visibilidadeSenha() {
    if (document.getElementById('login-password').type == 'password') {
        document.getElementById('login-password').type = 'text'
        document.getElementById('olho').src = "https://cdn4.iconfinder.com/data/icons/symbol-blue-set-1/100/Untitled-2-34-512.png"
    } else {
        document.getElementById('login-password').type = 'password'
        document.getElementById('olho').src = "https://cdn0.iconfinder.com/data/icons/ui-icons-pack/100/ui-icon-pack-14-512.png"
    }
}