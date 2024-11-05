CREATE VIEW FuncionariosFlorianopolis AS
SELECT codf, nome, cpf, idade
FROM Funcionarios
WHERE cidade = 'Florianopolis';

SELECT * FROM FuncionariosFlorianopolis;

UPDATE FuncionariosFlorianopolis
SET idade = idade + 1;

SELECT * FROM FuncionariosFlorianopolis;

INSERT INTO FuncionariosFlorianopolis (codf, nome, cpf, idade)
VALUES (10, 'Rodrigo', '22200022233', 41);

SELECT * FROM FuncionariosFlorianopolis;

CREATE OR REPLACE FUNCTION insert_funcionarios_florianopolis()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Funcionarios (codf, nome, cpf, idade, cidade)
    VALUES (NEW.codf, NEW.nome, NEW.cpf, NEW.idade, 'Florianopolis');
    RETURN NULL;  -- Retorna NULL para impedir a inserção direta na visão
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_insert_funcionarios_florianopolis
INSTEAD OF INSERT ON FuncionariosFlorianopolis
FOR EACH ROW
EXECUTE FUNCTION insert_funcionarios_florianopolis();

INSERT INTO FuncionariosFlorianopolis (codf, nome, cpf, idade)
VALUES (11, 'Raul', '44400044433', 53);

SELECT * FROM FuncionariosFlorianopolis;

CREATE VIEW MedicosAmbulatorio2 AS
SELECT codm, nome, idade, cpf, nroa
FROM Medicos
WHERE nroa >= 2
WITH CHECK OPTION;

SELECT * FROM MedicosAmbulatorio2;

INSERT INTO MedicosAmbulatorio2 (codm, nome, idade, cpf, nroa)
VALUES (7, 'Soraia', 47, '55500055533', 2);

SELECT * FROM MedicosAmbulatorio2;

INSERT INTO MedicosAmbulatorio2 (codm, nome, idade, cpf, nroa)
VALUES (8, 'Saulo', 52, '66600066633', 1);