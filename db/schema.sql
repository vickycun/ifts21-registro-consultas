-- BASE NUEVA para evitar modificar las tablas del ejemplo anterior.
-- Ejecutar UNA SOLA VEZ en MySQL Workbench.
CREATE DATABASE IF NOT EXISTS ejemplo_ifts DEFAULT CHARSET utf8mb4;
USE ejemplo_ifts;

CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(50) NOT NULL,
  edad INT NOT NULL
);

-- Si ya cargaste los 6 usuarios en el ejemplo anterior, no los duplica.
INSERT INTO usuarios (id, nombre, apellido, edad) VALUES
 (1,'Ana','García',30), (2,'Juan','López',45), (3,'María','López',28),
 (4,'Elena','Martínez',25), (5,'Pedro','Gómez',52), (6,'Lucía','García',19)
ON DUPLICATE KEY UPDATE id = id;

CREATE TABLE IF NOT EXISTS consultas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  descripcion TEXT NOT NULL,
  estado ENUM('pendiente','resuelta') NOT NULL DEFAULT 'pendiente',
  fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
