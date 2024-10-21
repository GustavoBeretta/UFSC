const router = require("express").Router()

const userController = require('../controllers/userController')

router.route("/create-user").post((req, res) => userController.create(req, res))

router.route("/check-user").post((req, res) => userController.checkUsername(req, res))

router.route("/login").post((req, res) => userController.login(req, res))

module.exports = router