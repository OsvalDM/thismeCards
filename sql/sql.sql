CREATE TABLE usuario (
    id VARCHAR(20),
    nombreUsuario VARCHAR(30),
    psw VARCHAR(200),
    admin BOOLEAN DEFAULT 0,
    PRIMARY KEY(id)
);

CREATE TABLE tarjeta (
    id INT AUTO_INCREMENT,
    nombre VARCHAR(40),
    apellidoPat VARCHAR(40),
    apellidoMat VARCHAR(40),
    correo VARCHAR(200),
    telefono VARCHAR(15),
    sobreMi VARCHAR(500),
    ubicacion VARCHAR(500),
    lat VARCHAR(100),
    lng VARCHAR(100),
    usuario VARCHAR(20),
    cargo VARCHAR(200),
    titulo VARCHAR(10),
    PRIMARY KEY(id),
    FOREIGN KEY(usuario) REFERENCES usuario(id)
);

CREATE TABLE redSocial(
    tarjeta INT,
    plataforma VARCHAR(30),
    nombre VARCHAR(100),
    FOREIGN KEY(tarjeta) REFERENCES tarjeta(id),
    PRIMARY KEY (tarjeta, plataforma)
);

CREATE TABLE imgPortafolio(
    tarjeta INT,
    rutaPortafolio VARCHAR(400),
    PRIMARY KEY ( tarjeta, rutaPortafolio ),
    FOREIGN KEY(tarjeta) REFERENCES tarjeta(id)
);

CREATE TABLE imgPerfil(
    tarjeta INT,
    rutaPerfil VARCHAR(400),
    PRIMARY KEY (tarjeta, rutaPerfil),
    FOREIGN KEY(tarjeta) REFERENCES tarjeta(id)
);

CREATE TABLE cliente(
    id INT AUTO_INCREMENT,
    nombre VARCHAR(200),
    imgLogo VARCHAR(400),
    tarjeta INT,
    PRIMARY KEY (id),
    FOREIGN KEY(tarjeta) REFERENCES tarjeta(id)
);

CREATE TABLE movimientos(
    id INT AUTO_INCREMENT,
    usuario VARCHAR(200),
    accion VARCHAR(200),
    fecha TIMESTAMP,
    PRIMARY KEY(id)
);

CREATE TABLE pregunta(
    id INT AUTO_INCREMENT,
    contenido VARCHAR(300),
    PRIMARY KEY(id)
);

CREATE TABLE recuperacionContrasena(
    id INT AUTO_INCREMENT,
    usuario VARCHAR(20),
    pregunta INT,
    respuesta VARCHAR(300),
    PRIMARY KEY(id),
    FOREIGN KEY (usuario) REFERENCES usuario(id),
    FOREIGN KEY (pregunta) REFERENCES pregunta(id)
);

INSERT INTO pregunta(contenido) VALUES
    ('¿En qué ciudad se conocieron tus padres?'),
    ('¿A qué primaria asististe?'),
    ('¿En qué lugar conociste a tu mejor amigo?'),
    ('¿A qué ciudad siempre quisiste ir?')
;