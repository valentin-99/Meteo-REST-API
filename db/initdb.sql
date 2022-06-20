CREATE DATABASE IF NOT EXISTS Meteo;
USE Meteo;

CREATE TABLE IF NOT EXISTS Tari (
    id int NOT NULL AUTO_INCREMENT,
    nume_tara varchar(20),
    latitudine double(8, 3) NOT NULL,
    longitudine double(8, 3) NOT NULL,
    PRIMARY KEY (id),
    unique(nume_tara)
);

CREATE TABLE IF NOT EXISTS Orase (
    id int NOT NULL AUTO_INCREMENT,
    id_tara int NOT NULL,
    nume_oras varchar(20),
    latitudine double(8, 3) NOT NULL,
    longitudine double(8, 3) NOT NULL,
    PRIMARY KEY (id),
    unique(id_tara, nume_oras),
    CONSTRAINT id_tara_id_fkey FOREIGN KEY (id_tara) references Tari(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Temperaturi (
    id int NOT NULL AUTO_INCREMENT,
    valoare double(8, 3) DEFAULT NULL,
    time_stamp DATETIME(3),
    id_oras int NOT NULL,
    PRIMARY KEY (id),
    unique(id_oras, time_stamp),
    CONSTRAINT id_oras_id_fkey FOREIGN KEY (id_oras) references Orase(id) ON DELETE CASCADE
);

