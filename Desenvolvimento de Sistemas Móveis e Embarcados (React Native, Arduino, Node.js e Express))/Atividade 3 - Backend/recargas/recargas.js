const express = require('express');
const app = express();
const axios = require('axios');

const bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

let porta = 8070;
app.listen(porta, () => {
 console.log('Servidor em execução na porta: ' + porta);
});

const sqlite3 = require('sqlite3');

var db = new sqlite3.Database('./recargas.db', (err) => {
        if (err) {
            console.log('ERRO: não foi possível acessar o banco de dados.');
            throw err;
        }
        console.log('Conectado ao SQLite!');
    });

db.run(`CREATE TABLE IF NOT EXISTS recargas
        (id INTEGER PRIMARY KEY, cpf TEXT NOT NULL, carga INTEGER NOT NULL, status TEXT NOT NULL, data DATETIME DEFAULT CURRENT_TIMESTAMP)`, 
        [], (err) => {
           if (err) {
              console.log('ERRO: não foi possível criar tabela.');
              throw err;
           }
      });

app.post('/recargas', async (req, res, next) => {

    try {
        const response = await axios.get(`http://localhost:8060/usuarios/${req.body.cpf}`)
        var cartao = response.data.cartao
    } catch (error) {
        if (error.response && error.response.status === 404) {
            res.status(404).send('Usuário não encontrado.');
        } else {
            console.error('Erro na comunicação com o serviço de usuários:', error.message);
            res.status(500).send('Erro ao verificar usuário.');
        }
        return
    }

    try {
        const response = await axios.post('http://localhost:8080/cobrancas', {carga: req.body.carga, cartao: cartao})
        var recarga = response.data.recarga
    } catch (error) {
        console.error('Erro na comunicação com o serviço de cobrança:', error.message);
        res.status(500).send('Erro ao realizar cobrança.');
        return
    }

    try {
        const response = await axios.post(`http://localhost:8090/estacoes/${req.body.carga}`)
        var status = "Concluída"
    } catch (error) {
        console.error('Erro na comunicação com a estação:', error.message);
        res.status(500).send('Erro ao carregar.');
        var status = "Não concluída"
    }

    db.run(`INSERT INTO recargas(id, cpf, carga, status) VALUES(?, ?, ?, ?)`, 
         [recarga, req.body.cpf, req.body.carga, status], (err) => {
        if (err) {
            console.log("Error: " + err);
            res.status(500).send('Erro ao cadastrar recarga.');
        } else {
            console.log('Recarga cadastrada com sucesso!');
            res.status(200).send('Recarga cadastrada com sucesso!');
        }
    });
});

app.get('/recargas', (req, res, next) => {
    db.all(`SELECT * FROM recargas`, [], (err, result) => {
        if (err) {
             console.log("Erro: " + err);
             res.status(500).send('Erro ao obter dados.');
        } else {
            res.status(200).json(result);
        }
    });
});

app.get('/recargas/id/:id', (req, res, next) => {
    db.get( `SELECT * FROM recargas WHERE id = ?`, 
            req.params.id, (err, result) => {
        if (err) { 
            console.log("Erro: "+err);
            res.status(500).send('Erro ao obter dados.');
        } else if (result == null) {
            console.log("Recarga não encontrada.");
            res.status(404).send('Recarga não encontrada.');
        } else {
            res.status(200).json(result);
        }
    });
});

app.get('/recargas/cpf/:cpf', (req, res, next) => {
    db.get( `SELECT * FROM recargas WHERE cpf = ?`, 
            req.params.cpf, (err, result) => {
        if (err) { 
            console.log("Erro: "+err);
            res.status(500).send('Erro ao obter dados.');
        } else if (result == null) {
            console.log("Nenhuma recarga foi encontrada.");
            res.status(404).send('Nenhuma recarga foi encontrada.');
        } else {
            res.status(200).json(result);
        }
    });
});