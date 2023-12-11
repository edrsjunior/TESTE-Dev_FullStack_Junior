CREATE DATABASE IF NOT EXISTS verzel_cars;
USE verzel_cars;

CREATE TABLE IF NOT EXISTS veiculosAnuncio(
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(20) NOT NULL,
    valor FLOAT NOT NULL,
    descricao VARCHAR(500),
    photoUrl VARCHAR(200) NOT NULL,
    creator INT,
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
    token VARCHAR(255),
    modificationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY(id)
);

SELECT * FROM usuario;
SELECT * FROM veiculosAnuncio;

DROP TABLE veiculosAnuncio;
DROP TABLE usuario;


