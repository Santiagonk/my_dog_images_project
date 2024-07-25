import requests
import threading
import time
from PIL import Image
from io import BytesIO
import os
import psycopg2
from app.db.db_connection import DatabaseConnection


if not os.path.exists('dog_images'):
    os.makedirs('dog_images')


def download_image(url, filename):
    """Función para descargar una imagen y guardarla en el disco."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))
        img.save(filename)
        print(f"Imagen guardada: {filename}")

    except Exception as e:
        print(f"Error al descargar o guardar la imagen {filename}: {e}")


def fetch_image_url():
    """Función para obtener la URL de una imagen de la API."""
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        response.raise_for_status()
        data = response.json()
        return data['message']
    except Exception as e:
        print(f"Error al obtener URL de la imagen: {e}")
        return None


def save_url(url, filename, index):
    db = DatabaseConnection()
    conn = None
    try:
        conn = db.create_connection()
        with conn.cursor() as cursor:
            query = psycopg2.sql.SQL(
                f"INSERT INTO Imagen VALUES ({index}, '{url}', '{filename}')")
            cursor.execute(query)
            return True
    except psycopg2.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
    finally:
        db.close_connection(conn)


def worker(index):
    """
    Función del hilo que descarga una imagen y la guarda en el directorio.
    """
    url = fetch_image_url()
    filename = f'dog_images/image_{index}.jpg'
    if not save_url(url, filename, index):
        raise Exception('No se pudo guardar el registro')
    if url:
        download_image(url, filename)


def main():
    """
    Función principal para gestionar la descarga de imágenes con
    multithreading.
    """
    start_time = time.time()

    threads = []
    num_threads = 10

    for i in range(50):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

        if len(threads) >= num_threads:
            for thread in threads:
                thread.join()
            threads = []

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Tiempo total de ejecución: {end_time - start_time:.2f} segundos")


if __name__ == "__main__":
    main()
