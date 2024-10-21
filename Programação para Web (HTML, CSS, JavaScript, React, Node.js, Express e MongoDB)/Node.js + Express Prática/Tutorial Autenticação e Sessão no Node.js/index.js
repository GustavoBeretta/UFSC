const express = require('express');
const session = require('express-session')
const passport = require('passport');
    
const app = express();
app.use(session({
    secret: 'jojoba',
    saveUninitialized:true,
    resave: false
}))
app.use(passport.initialize())
app.use(passport.session())

app.get('/', (req, res) => {
    res.send('<a href="/auth/google">Autenticar com Google</a>')
})

app.get('/auth/google', 
    passport.authenticate('google', {
        scope: ['email', 'profile']
    })
)

app.get('/google/callback',
    passport.authenticate('google', {
        successRedirect: '/segredo',
        failureRedirect: '/auth/falha'
    })
)

app.get('/segredo', usuarioLogado, (req, res) => {
    res.send(`Segredo aqui... Olá ${req.user.displayName}. <a href=/logout>Logout</a>`)
})

function usuarioLogado(req, res, next) {
    req.user ? next() : res.sendStatus(401)
}

app.get('/auth/falha', (req, res) => {
    res.send("Falha de autenticação.")
})

app.get('/logout', (req, res) => {
    req.session.destroy()
    res.send("Até mais!")
})

app.listen(5000, () => {
    console.log("Servidor iniciado")
})