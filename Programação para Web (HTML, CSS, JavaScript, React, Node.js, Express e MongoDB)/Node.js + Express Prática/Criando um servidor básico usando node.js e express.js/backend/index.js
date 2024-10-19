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

app.listen(3125, ()=>console.log("Listening on port 3125"))