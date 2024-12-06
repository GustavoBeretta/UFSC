const express = require('express');
const app = express();

const bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

let porta = 8080;
app.listen(porta, () => {
 console.log('Servidor em execução na porta: ' + porta);
});

const sqlite3 = require('sqlite3');

var db = new sqlite3.Database('./cobrancas.db', (err) => {
        if (err) {
            console.log('ERRO: não foi possível acessar o banco de dados.');
            throw err;
        }
        console.log('Conectado ao SQLite!');
    });

db.run(`CREATE TABLE IF NOT EXISTS cobrancas
        (recarga INTEGER PRIMARY KEY AUTOINCREMENT, valor REAL NOT NULL, cartao TEXT NOT NULL)`, 
        [], (err) => {
           if (err) {
              console.log('ERRO: não foi possível criar tabela.');
              throw err;
           }
      });

app.post('/cobrancas', (req, res, next) => {
    db.run(`INSERT INTO cobrancas(valor, cartao) VALUES(?, ?)`, 
         [req.body.carga * 2, req.body.cartao], function(err) {
        if (err) {
            console.log("Error: " + err);
            res.status(500).send('Erro ao realizar cobrança.');
        } else {
            console.log(`Cobrança realizada com sucesso no cartão ${req.body.cartao}!`);
            res.status(200).send({message: `Cobrança realizada com sucesso no cartão ${req.body.cartao}!`, recarga: this.lastID});
        }
    });
});

app.get('/cobrancas', (req, res, next) => {
    db.all(`SELECT * FROM cobrancas`, [], (err, result) => {
        if (err) {
             console.log("Erro: " + err);
             res.status(500).send('Erro ao obter dados.');
        } else {
            res.status(200).json(result);
        }
    });
});

app.get('/cobrancas/:recarga', (req, res, next) => {
    db.get( `SELECT * FROM cobrancas WHERE recarga = ?`, 
            req.params.recarga, (err, result) => {
        if (err) { 
            console.log("Erro: "+err);
            res.status(500).send('Erro ao obter dados.');
        } else if (result == null) {
            console.log("Cobrança não encontrada.");
            res.status(404).send('Cobrança não encontrada.');
        } else {
            res.status(200).json(result);
        }
    });
});