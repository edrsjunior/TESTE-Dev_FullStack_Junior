CREATE DATABASE IF NOT EXISTS verzel_cars;
USE verzel_cars;

CREATE TABLE IF NOT EXISTS veiculosAnuncio(
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(20) NOT NULL,
    ano int NOT NULL,
    km float NOT NULL,
    valor FLOAT NOT NULL,
    descricao VARCHAR(500),
    photoUrl VARCHAR(200),
    creator INT,
    modificationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id),
    FOREIGN KEY (creator) REFERENCES usuario(id)
);

CREATE TABLE IF NOT EXISTS usuario(
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(20) NOT NULL,
    sobrenome VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    isAdmin BOOLEAN DEFAULT False,
    modificationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY(id)
);

UPDATE usuario SET isAdmin = 1 WHERE email = "admin001.com";

SELECT * FROM usuario;
SELECT * FROM veiculosAnuncio;

DROP TABLE veiculosAnuncio;
DROP TABLE usuario;

UPDATE usuario 
SET ativo= TRUE
WHERE id = 1; 