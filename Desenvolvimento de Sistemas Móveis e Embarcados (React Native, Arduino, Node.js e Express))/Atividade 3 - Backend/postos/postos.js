const express = require('express');
const app = express();

const bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

let porta = 8050;
app.listen(porta, () => {
 console.log('Servidor em execução na porta: ' + porta);
});

const sqlite3 = require('sqlite3');

var db = new sqlite3.Database('./postos.db', (err) => {
        if (err) {
            console.log('ERRO: não foi possível acessar o banco de dados.');
            throw err;
        }
        console.log('Conectado ao SQLite!');
    });

db.run(`CREATE TABLE IF NOT EXISTS postos
        (id INTEGER PRIMARY KEY AUTOINCREMENT, endereco TEXT NOT NULL UNIQUE)`, 
        [], (err) => {
           if (err) {
              console.log('ERRO: não foi possível criar tabela.');
              throw err;
           }
      });

app.post('/postos', (req, res, next) => {
    db.run(`INSERT INTO postos(endereco) VALUES(?)`, 
         [req.body.endereco], (err) => {
        if (err) {
            console.log("Error: " + err);
            res.status(500).send('Erro ao cadastrar posto.');
        } else {
            console.log('Posto cadastrado com sucesso!');
            res.status(200).send('Posto cadastrado com sucesso!');
        }
    });
});

app.get('/postos', (req, res, next) => {
    db.all(`SELECT * FROM postos`, [], (err, result) => {
        if (err) {
             console.log("Erro: " + err);
             res.status(500).send('Erro ao obter dados.');
        } else {
            res.status(200).json(result);
        }
    });
});

app.get('/postos/:id', (req, res, next) => {
    db.get( `SELECT * FROM postos WHERE id = ?`, 
            req.params.id, (err, result) => {
        if (err) { 
            console.log("Erro: "+err);
            res.status(500).send('Erro ao obter dados.');
        } else if (result == null) {
            console.log("Posto não encontrado.");
            res.status(404).send('Posto não encontrado.');
        } else {
            res.status(200).json(result);
        }
    });
});

app.patch('/postos/:id', (req, res, next) => {
    db.run(`UPDATE postos SET endereco = ? WHERE id = ?`,
           [req.body.endereco, req.params.id], function(err) {
            if (err){
                res.status(500).send('Erro ao alterar dados.');
            } else if (this.changes == 0) {
                console.log("Posto não encontrado.");
                res.status(404).send('Posto não encontrado.');
            } else {
                res.status(200).send('Endereço alterado com sucesso!');
            }
    });
});

app.delete('/postos/:id', (req, res, next) => {
    db.run(`DELETE FROM postos WHERE id = ?`, req.params.id, function(err) {
      if (err){
         res.status(500).send('Erro ao remover posto.');
      } else if (this.changes == 0) {
         console.log("Posto não encontrado.");
         res.status(404).send('Posto não encontrado.');
      } else {
         res.status(200).send('Posto removido com sucesso!');
      }
   });
});