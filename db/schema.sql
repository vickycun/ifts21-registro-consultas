
-- Base de datos alojada en Aiven
USE defaultdb;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(50) NOT NULL,
  edad INT NOT NULL
);

-- Datos iniciales de prueba
INSERT INTO usuarios (id, nombre, apellido, edad) VALUES
 (1,'Ana','García',30),
 (2,'Juan','López',45),
 (3,'María','López',28),
 (4,'Elena','Martínez',25),
 (5,'Pedro','Gómez',52),
 (6,'Lucía','García',19)
ON DUPLICATE KEY UPDATE id = id;

-- Tabla de consultas
CREATE TABLE IF NOT EXISTS consultas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  descripcion TEXT NOT NULL,
  estado ENUM('pendiente','resuelta') NOT NULL DEFAULT 'pendiente',
  fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
