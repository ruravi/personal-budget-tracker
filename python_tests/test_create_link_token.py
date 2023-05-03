from http.server import HTTPServer
from threading import Thread
import unittest
from api.plaid_helper import handler
import requests


class TestCreateLinkToken(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_server = HTTPServer(('localhost', 8082), handler)
        # Start running mock server in a separate thread.
        # Daemon threads automatically shut down when the main process exits.
        self.mock_server_thread = Thread(target=self.mock_server.serve_forever)
        self.mock_server_thread.setDaemon(True)
        self.mock_server_thread.start()

    def test_create_link_token(self):
        actual_response = requests.get('http://localhost:8082')
        self.assertEqual(actual_response.status_code, 200)
        self.assertEqual(actual_response.text, 'Hello, world!')
