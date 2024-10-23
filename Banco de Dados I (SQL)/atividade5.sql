SELECT nome 
FROM pacientes 
WHERE codp IN (
    SELECT codp 
    FROM consultas 
    WHERE EXTRACT(HOUR FROM hora) > 14
);

SELECT nome, idade 
FROM medicos 
WHERE codm IN (
    SELECT codm 
    FROM consultas 
    WHERE codp IN (
        SELECT codp 
        FROM pacientes 
        WHERE nome = 'Ana'
    )
);

SELECT nroa, andar 
FROM ambulatorios 
WHERE nroa NOT IN (
    SELECT DISTINCT nroa 
    FROM medicos
    WHERE nroa IS NOT NULL
);

SELECT cpf 
FROM medicos 
WHERE nroa = SOME (
    SELECT nroa 
    FROM ambulatorios 
    WHERE andar = 1
);

SELECT nome, CPF
FROM funcionarios
WHERE nome NOT IN (
	SELECT nome
	FROM funcionarios
	WHERE salario >= ALL (SELECT salario FROM funcionarios)
);

SELECT nome 
FROM pacientes 
WHERE codp IN (
    SELECT codp 
    FROM consultas 
    WHERE hora < ALL (
        SELECT hora 
        FROM consultas 
        WHERE data = '2020-10-14'
    )
);

SELECT nroa, andar 
FROM ambulatorios 
WHERE capacidade > ALL (
    SELECT capacidade 
    FROM ambulatorios 
    WHERE andar = 1
);