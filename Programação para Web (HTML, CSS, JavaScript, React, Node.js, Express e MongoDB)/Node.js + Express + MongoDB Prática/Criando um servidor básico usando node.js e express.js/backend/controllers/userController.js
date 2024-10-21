const { User: UserModel } = require('../models/User')

const userController = {

    create: async(req, res) => {
        try {

            const user = {
                username: req.body.username,
                nome: req.body.nome,
                sobrenome: req.body.sobrenome,
                email: req.body.email,
                senha: req.body.senha,
                cep: req.body.cep
            }

            const response = await UserModel.create(user)

            res.status(201).json({response, msg: 'Usuário criado com sucesso!'})

        } catch (error) {
            console.log(error)
        }
    },

    checkUsername: async (req, res) => {
        try {

            let username = req.body.username

            const users = await UserModel.find()
            
            const userExists = users.some(user => user.username === username);

            if (userExists) {
                console.log('Usuário já existente');
                return res.status(200).json({ userExists: true });
            } else {
                console.log('Usuário não encontrado');
                return res.status(200).json({ userExists: false });
            }

        } catch (error) {
            console.log(error)
        }
    },

    login: async (req, res) => {
        try {

            let email = req.body.email
            let senha = req.body.senha

            const users = await UserModel.find()

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

        } catch (error) {
            console.log(error)
        }
    }

}

module.exports = userController