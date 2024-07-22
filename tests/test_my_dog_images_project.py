import unittest
from unittest.mock import patch, MagicMock
import requests
from app.main import download_image, fetch_image_url, worker


class TestMyDogImagesProject(unittest.TestCase):

    @patch('app.main.requests.get')
    def test_fetch_image_url_success(self, mock_get):
        """
        Prueba si fetch_image_url devuelve la URL de la imagen correctamente.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'message': 'https://example.com/dog.jpg'}
        mock_get.return_value = mock_response

        url = fetch_image_url()
        self.assertEqual(url, 'https://example.com/dog.jpg')

    @patch('app.main.requests.get')
    def test_fetch_image_url_failure(self, mock_get):
        """
        Prueba la función fetch_image_url cuando hay un error en la solicitud.
        """
        mock_get.side_effect = requests.exceptions.RequestException("Error")

        url = fetch_image_url()
        self.assertIsNone(url)

    @patch('app.main.requests.get')
    @patch('app.main.Image.open')
    @patch('app.main.Image.save')
    def test_download_image_success(self, mock_save, mock_open, mock_get):
        """
        Prueba si download_image descarga y guarda la imagen correctamente.
        """
        mock_response = MagicMock()
        mock_response.content = b'image_data'
        mock_get.return_value = mock_response
        mock_image = MagicMock()
        mock_open.return_value = mock_image

        download_image('https://example.com/dog.jpg', 'test_image.jpg')
        mock_get.assert_called_once_with('https://example.com/dog.jpg')
        mock_open.assert_called_once()
        mock_image.save.assert_called_once_with('test_image.jpg')

    @patch('app.main.fetch_image_url')
    @patch('app.main.download_image')
    def test_worker_function(self, mock_download, mock_fetch):
        """
        Prueba si la función worker llama a fetch_image_url y download_image
        correctamente.
        """
        mock_fetch.return_value = 'https://example.com/dog.jpg'
        worker(1)
        mock_fetch.assert_called_once()
        mock_download.assert_called_once_with(
            'https://example.com/dog.jpg', 'dog_images/dog_image_1.jpg')


if __name__ == '__main__':
    unittest.main()
