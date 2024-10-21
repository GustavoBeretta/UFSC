const express = require('express')
const cors = require('cors')
const app = express()

app.use(cors({
    origin: '*'
}));

app.use(express.json())

const conn = require('./db/conn')

conn()

const routes = require("./routes/router")

app.use("/api", routes)

app.listen(3125, ()=>console.log("Listening on port 3125"))