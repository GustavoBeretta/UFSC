const express = require('express');
const app = express();

const bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

let porta = 8090;
app.listen(porta, () => {
 console.log('Servidor em execução na porta: ' + porta);
});

app.post('/estacoes/:carga', (req, res, next) => {
    try {
        console.log(`Estação liberada. Iniciando carregamento de ${req.params.carga}kWh.`)

        for (let i = 1; i < req.params.carga; i++) {
            setTimeout(() => {
                console.log(`Carregamento em andamento: ${((i/req.params.carga)*100).toFixed(0)}%`)
            }, i * 100)
        }

        setTimeout(() => {
            console.log('Carregamento concluído. Estação bloqueada novamente.')
        }, req.params.carga * 100)

        res.status(200).send('Recarga concluída com sucesso!')
    } catch (error) {
        res.status(500).send('Erro ao realizar recarga.');
    }
});