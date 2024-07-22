CREATE DATABASE my_dogs_images_project;

\c my_dogs_images_project

CREATE TABLE Imagen (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    nombre_archivo TEXT,
    fecha_descarga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
