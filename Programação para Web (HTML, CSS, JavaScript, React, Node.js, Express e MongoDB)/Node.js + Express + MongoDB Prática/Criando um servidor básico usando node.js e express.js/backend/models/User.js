const mongoose = require('mongoose')

const { Schema } = mongoose

const userSchema = new Schema(
    {
        username: String,
        nome: String,
        sobrenome: String,
        email: String,
        senha: String,
        cep: String,
    },
);

const User =  mongoose.model("User", userSchema)

module.exports = {User, userSchema}