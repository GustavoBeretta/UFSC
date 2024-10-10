SELECT Medicos.nome, Medicos.CPF
FROM Medicos
JOIN Pacientes ON Medicos.CPF = Pacientes.CPF;

SELECT Funcionarios.nome AS Funcionario, Medicos.nome AS Medico
FROM Funcionarios
JOIN Medicos ON Funcionarios.cidade = Medicos.cidade;

SELECT Medicos.nome, Medicos.idade
FROM Medicos
JOIN Consultas ON Medicos.codm = Consultas.codm
JOIN Pacientes ON Consultas.codp = Pacientes.codp
WHERE Pacientes.nome = 'Ana';

SELECT Ambulatorios.nroa
FROM Ambulatorios
JOIN Ambulatorios AS A ON Ambulatorios.andar = A.andar
WHERE A.nroa = 5;

SELECT Pacientes.codp, Pacientes.nome
FROM Pacientes
NATURAL JOIN Consultas
WHERE Consultas.hora > '14:00:00';

SELECT Ambulatorios.nroa, Ambulatorios.andar
FROM Ambulatorios
NATURAL JOIN Medicos
NATURAL JOIN Consultas
WHERE Consultas.data = '2020-10-12';

SELECT Ambulatorios.*, Medicos.codm, Medicos.nome
FROM Ambulatorios
LEFT JOIN Medicos ON Ambulatorios.nroa = Medicos.nroa;

SELECT Medicos.CPF, Medicos.nome, Pacientes.nome AS paciente_nome, Consultas.data
FROM Medicos
LEFT JOIN Consultas ON Medicos.codm = Consultas.codm
LEFT JOIN Pacientes ON Consultas.codp = Pacientes.codp;