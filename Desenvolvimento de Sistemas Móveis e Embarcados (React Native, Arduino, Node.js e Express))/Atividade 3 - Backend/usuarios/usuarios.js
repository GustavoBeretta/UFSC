const express = require('express');
const app = express();

const bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

let porta = 8060;
app.listen(porta, () => {
 console.log('Servidor em execução na porta: ' + porta);
});

const sqlite3 = require('sqlite3');

var db = new sqlite3.Database('./usuarios.db', (err) => {
        if (err) {
            console.log('ERRO: não foi possível acessar o banco de dados.');
            throw err;
        }
        console.log('Conectado ao SQLite!');
    });

db.run(`CREATE TABLE IF NOT EXISTS usuarios
        (cpf TEXT PRIMARY KEY, nome TEXT NOT NULL, email TEXT NOT NULL, cartao TEXT NOT NULL)`, 
        [], (err) => {
           if (err) {
              console.log('ERRO: não foi possível criar tabela.');
              throw err;
           }
      });

app.post('/usuarios', (req, res, next) => {
    db.run(`INSERT INTO usuarios(cpf, nome, email, cartao) VALUES(?, ?, ?, ?)`, 
         [req.body.cpf, req.body.nome, req.body.email, req.body.cartao], (err) => {
        if (err) {
            console.log("Error: " + err);
            res.status(500).send('Erro ao cadastrar usuário.');
        } else {
            console.log('Usuário cadastrado com sucesso!');
            res.status(200).send('Usuário cadastrado com sucesso!');
        }
    });
});

app.get('/usuarios', (req, res, next) => {
    db.all(`SELECT * FROM usuarios`, [], (err, result) => {
        if (err) {
             console.log("Erro: " + err);
             res.status(500).send('Erro ao obter dados.');
        } else {
            res.status(200).json(result);
        }
    });
});

app.get('/usuarios/:cpf', (req, res, next) => {
    db.get( `SELECT * FROM usuarios WHERE cpf = ?`, 
            req.params.cpf, (err, result) => {
        if (err) { 
            console.log("Erro: "+err);
            res.status(500).send('Erro ao obter dados.');
        } else if (result == null) {
            console.log("Usuário não encontrado.");
            res.status(404).send('Usuário não encontrado.');
        } else {
            res.status(200).json(result);
        }
    });
});

app.patch('/usuarios/:cpf', (req, res, next) => {
    db.run(`UPDATE usuarios SET nome = ?, email = ?, cartao = ? WHERE cpf = ?`,
        [req.body.nome, req.body.email, req.body.cartao, req.params.cpf], function(err) {
            if (err){
                res.status(500).send('Erro ao alterar dados.');
            } else if (this.changes == 0) {
                console.log("Usuário não encontrado.");
                res.status(404).send('Usuário não encontrado.');
            } else {
                res.status(200).send('Usuário alterado com sucesso!');
            }
    });
});

app.delete('/usuarios/:cpf', (req, res, next) => {
    db.run(`DELETE FROM usuarios WHERE cpf = ?`, req.params.cpf, function(err) {
      if (err){
         res.status(500).send('Erro ao remover usuário.');
      } else if (this.changes == 0) {
         console.log("Usuário não encontrado.");
         res.status(404).send('Usuário não encontrado.');
      } else {
         res.status(200).send('Usuário removido com sucesso!');
      }
   });
});