SELECT *
FROM Funcionarios
ORDER BY salario DESC, idade ASC
LIMIT 3;

SELECT Medicos.nome AS nome_medico, Ambulatorios.nroa, Ambulatorios.andar
FROM Medicos
JOIN Ambulatorios ON Medicos.nroa = Ambulatorios.nroa
ORDER BY Ambulatorios.nroa;

SELECT andar, SUM(capacidade) AS capacidade_total
FROM Ambulatorios
GROUP BY andar;

SELECT andar
FROM Ambulatorios
GROUP BY andar
HAVING AVG(capacidade) >= 40;

SELECT Medicos.nome
FROM Medicos
JOIN Consultas ON Medicos.codm = Consultas.codm
GROUP BY Medicos.nome
HAVING COUNT(Consultas.codp) > 1;

DELETE FROM Ambulatorios
WHERE nroa NOT IN (SELECT nroa FROM Medicos);

UPDATE Medicos
SET cidade = (SELECT cidade FROM Pacientes WHERE nome = 'Paulo'),
    idade = (SELECT idade * 2 FROM Pacientes WHERE nome = 'Ana')
WHERE nome = 'Pedro';

INSERT INTO Medicos (codm, CPF, nome, idade, cidade, especialidade, nroa)
SELECT 5, Funcionarios.CPF, Funcionarios.nome, Funcionarios.idade, Funcionarios.cidade, Medicos.especialidade, Medicos.nroa
FROM Funcionarios
JOIN Medicos ON Medicos.codm = 2
WHERE Funcionarios.nome = 'Caio' AND Funcionarios.codf = 3;
DELETE FROM funcionarios WHERE nome = 'Caio';
