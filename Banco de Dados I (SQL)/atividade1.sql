CREATE TABLE Ambulatorios (
	nroa int,
	andar numeric(2) NOT NULL,
	capacidade smallint,
	PRIMARY KEY(nroa)
);

CREATE TABLE Medicos (
	codm int,
	nome varchar(40) NOT NULL,
	idade smallint NOT NULL,
	cidade varchar(40),
	CPF numeric(11) NOT NULL UNIQUE,
	especialidade varchar(30),
	nroa int,
	PRIMARY KEY (codm),
	FOREIGN KEY (nroa) REFERENCES Ambulatorios
);

CREATE TABLE Pacientes (
	codp int,
	nome varchar(40) NOT NULL,
	idade smallint NOT NULL,
	cidade varchar(40),
	CPF numeric(11) NOT NULL UNIQUE,
	doenca varchar(40) NOT NULL,
	PRIMARY KEY (codp)
);

CREATE TABLE Funcionarios (
	codf int,
	nome varchar(40) NOT NULL,
	idade smallint NOT NULL,
	cidade varchar(40),
	CPF numeric(11) NOT NULL UNIQUE,
	salario numeric(10),
	cargo varchar(40),
	PRIMARY KEY (codf)
);

CREATE TABLE Consultas (
	codm int,
	codp int,
	data date,
	hora time,
	PRIMARY KEY(codm, codp, data),
	FOREIGN KEY(codm) REFERENCES Medicos,
	FOREIGN KEY(codp) REFERENCES Pacientes
);

ALTER TABLE Funcionarios
	DROP COLUMN cargo;

CREATE INDEX indPac_cidade ON Pacientes(cidade);