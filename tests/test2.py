import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.preprocessor import Preprocessor, NORMALIZATION_DICT

class ClassUnitTest(unittest.TestCase):

    def setUp(self):
        # Setup for preprocessor test
        self.preprocessor = Preprocessor(NORMALIZATION_DICT)
        # Setup FastAPI TestClient
        self.client = TestClient(app)

    def test_preprocessor(self):
        post = "pls click 👉🏼https://:www.abcd.com for more details! "
        expected_res = "please click 👉🏼<URL> details"

        # Test using public method
        res = self.preprocessor.transform([post])[0]

        self.assertEqual(res, expected_res)

    def test_predict(self):
        # Prepare input
        test_data = {"post": "Win free recharge now!"}

        # Send POST request to FastAPI
        response = self.client.post("/predict", json=test_data)

        # Check response status
        self.assertEqual(response.status_code, 200)

        # Check response keys
        response_json = response.json()
        self.assertIn("label", response_json)
        self.assertIn("confidence", response_json)

        # Check label and confidence validity
        self.assertIn(response_json["label"], ["spam", "not_spam"])
        self.assertTrue(0.0 <= response_json["confidence"] <= 1.0)


if __name__ == '__main__':
    unittest.main()
