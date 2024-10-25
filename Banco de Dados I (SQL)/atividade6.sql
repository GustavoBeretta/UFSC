
SELECT nome, cpf 
FROM medicos m
WHERE EXISTS (
    SELECT 1 
    FROM pacientes p
    WHERE p.cpf = m.cpf
);

SELECT m.nome, m.cpf,
       CASE 
           WHEN EXISTS (
               SELECT 1
               FROM consultas sub
               LEFT JOIN pacientes sub_p ON sub.codp = sub_p.codp
               WHERE sub.codm = m.codm
                 AND sub_p.nome = 'Ana'
           ) THEN c.data
           ELSE NULL
       END AS data
FROM medicos m
LEFT JOIN consultas c ON m.codm = c.codm
WHERE m.especialidade = 'ortopedia'
ORDER BY m.nome, c.data;

SELECT m.nome, m.cpf
FROM medicos m
WHERE NOT EXISTS (
    SELECT 1
    FROM pacientes p
    WHERE NOT EXISTS (
        SELECT 1
        FROM consultas c
        WHERE c.codm = m.codm AND c.codp = p.codp
    )
);

SELECT m.nome, m.cpf
FROM medicos m
WHERE m.especialidade = 'ortopedia'
  AND NOT EXISTS (
    SELECT 1
    FROM pacientes p
    WHERE p.cidade = 'Florianopolis'
      AND NOT EXISTS (
        SELECT 1
        FROM consultas c
        WHERE c.codm = m.codm AND c.codp = p.codp
      )
);

SELECT sub.data, sub.hora
FROM (
    SELECT c.data, c.hora
    FROM consultas c
    JOIN medicos m ON c.codm = m.codm
    WHERE m.nome = 'Maria'
) sub;

SELECT DISTINCT sub.nome, sub.cidade
FROM (
    SELECT p.nome, p.cidade
    FROM pacientes p
    JOIN consultas c ON p.codp = c.codp
    JOIN medicos m ON c.codm = m.codm
    WHERE m.especialidade = 'ortopedia'
) sub;

SELECT m.nome, m.cpf
FROM medicos m
JOIN (
    SELECT nroa
    FROM medicos
    WHERE nome = 'Pedro'
) mp ON m.nroa = mp.nroa
WHERE m.nome != 'Pedro';
