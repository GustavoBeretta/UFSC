const express = require('express')
const cors = require('cors')
const app = express()

let users = []

app.use(cors({
    origin: '*'
}));

app.use(express.json())

app.post('/check-user', (req, res) => {

    let username = req.body.username

    console.log('Username:', username)

    const userExists = users.some(user => user.username === username);

    if (userExists) {
        console.log('Usuário já existente');
        return res.status(200).json({ userExists: true });
    } else {
        console.log('Usuário não encontrado');
        return res.status(200).json({ userExists: false });
    }
})

app.post('/create-user', (req, res) => {

    users.push(req.body)

    console.log('Usuário cadastrado com sucesso')
    console.log(users)

    res.status(201).json({ message: 'Usuário cadastrado com sucesso' })
})

app.post('/login', (req, res) => {

    let email = req.body.email
    let senha = req.body.senha

    for (let i = 0; i < users.length; i++) {
        if (users[i].email == email) {
            if (users[i].senha == senha) {
                return res.status(200).json({ message: 'Login realizado com sucesso com sucesso', usuario: users[i] });
            } else {
                return res.status(401).json({ message: 'Senha incorreta' });
            }
        }
    }

    return res.status(401).json({ message: 'Email não registrado' })
})

app.listen(3125, ()=>console.log("Listening on port 3125"))