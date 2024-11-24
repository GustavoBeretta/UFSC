// Inicia o Express.js
const express = require('express');
const app = express();

// Body Parser - usado para processar dados da requisição HTTP
const bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

// Método HTTP GET /hello - envia a mensagem: Hello World
app.get('/hello', (req, res) => {
 res.send('Hello World');
});

// Inicia o Servidor na porta 8080
let porta = 8080;
app.listen(porta, () => {
 console.log('Servidor em execução na porta: ' + porta);
});

// Importa o package do SQLite
const sqlite3 = require('sqlite3');

// Acessa o arquivo com o banco de dados
var db = new sqlite3.Database('./dados.db', (err) => {
        if (err) {
            console.log('ERRO: não foi possível conectar ao SQLite.');
            throw err;
        }
        console.log('Conectado ao SQLite!');
    });

// Cria a tabela cadastro, caso ela não exista
db.run(`CREATE TABLE IF NOT EXISTS cadastro 
        (nome TEXT NOT NULL, email TEXT NOT NULL, 
         cpf INTEGER PRIMARY KEY NOT NULL UNIQUE)`, 
        [], (err) => {
           if (err) {
              console.log('ERRO: não foi possível criar tabela.');
              throw err;
           }
      });    

// Método HTTP POST /Cadastro - cadastra um novo cliente
app.post('/Cadastro', (req, res, next) => {
    db.run(`INSERT INTO cadastro(nome, email, cpf) VALUES(?,?,?)`, 
         [req.body.nome, req.body.email, req.body.cpf], (err) => {
        if (err) {
            console.log("Error: " + err);
            res.status(500).send('Erro ao cadastrar cliente.');
        } else {
            console.log('Cliente cadastrado com sucesso!');
            res.status(200).send('Cliente cadastrado com sucesso!');
        }
    });
});

// Método HTTP GET /Cadastro - retorna todos os cadastros
app.get('/Cadastro', (req, res, next) => {
    db.all(`SELECT * FROM cadastro`, [], (err, result) => {
        if (err) {
             console.log("Erro: " + err);
             res.status(500).send('Erro ao obter dados.');
        } else {
            res.status(200).json(result);
        }
    });
});

// Método HTTP GET /Cadastro/:cpf - retorna cadastro do cliente com base no CPF
app.get('/Cadastro/:cpf', (req, res, next) => {
    db.get( `SELECT * FROM cadastro WHERE cpf = ?`, 
            req.params.cpf, (err, result) => {
        if (err) { 
            console.log("Erro: "+err);
            res.status(500).send('Erro ao obter dados.');
        } else if (result == null) {
            console.log("Cliente não encontrado.");
            res.status(404).send('Cliente não encontrado.');
        } else {
            res.status(200).json(result);
        }
    });
});

// Método HTTP GET /Cadastro - retorna todos os cadastros
app.get('/Cadastro', (req, res, next) => {
    db.all(`SELECT * FROM cadastro`, [], (err, result) => {
        if (err) {
             console.log("Erro: " + err);
             res.status(500).send('Erro ao obter dados.');
        } else {
            res.status(200).json(result);
        }
    });
});

// Método HTTP GET /Cadastro/:cpf - retorna cadastro do cliente com base no CPF
app.get('/Cadastro/:cpf', (req, res, next) => {
    db.get( `SELECT * FROM cadastro WHERE cpf = ?`, 
            req.params.cpf, (err, result) => {
        if (err) { 
            console.log("Erro: "+err);
            res.status(500).send('Erro ao obter dados.');
        } else if (result == null) {
            console.log("Cliente não encontrado.");
            res.status(404).send('Cliente não encontrado.');
        } else {
            res.status(200).json(result);
        }
    });
});

//Método HTTP DELETE /Cadastro/:cpf - remove um cliente do cadastro
app.delete('/Cadastro/:cpf', (req, res, next) => {
    db.run(`DELETE FROM cadastro WHERE cpf = ?`, req.params.cpf, function(err) {
      if (err){
         res.status(500).send('Erro ao remover cliente.');
      } else if (this.changes == 0) {
         console.log("Cliente não encontrado.");
         res.status(404).send('Cliente não encontrado.');
      } else {
         res.status(200).send('Cliente removido com sucesso!');
      }
   });
});