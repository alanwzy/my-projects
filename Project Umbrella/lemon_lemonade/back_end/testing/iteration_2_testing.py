import unittest
import requests
import ast

# For Iteration 2 /uvr_location_i2
class UVLocationI2(unittest.TestCase):

    # Check the structure of response
    def test_response_structure(self):
        expected_structure = ["postcode", "suburb", "UVR", "max_UVR", "lat", "lng"]

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/uvr_location_i2", params={"postcode": 3000})
        data = ast.literal_eval(req.text)
        data_structure = list(data.keys())

        self.assertEqual(data_structure, expected_structure)


# For Iteration 2 /nearby_hospitals_i2
class NearbyHospitalI2(unittest.TestCase):

    # Check the length of response
    def test_response_length(self):
        minimum_length = 1

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/nearby_hospitals_i2", params={"postcode": 3000})
        data = ast.literal_eval(req.text)
        data_length = len(data)

        self.assertTrue(data_length >= minimum_length)

    # Check the structure of response
    def test_response_structure(self):
        expected_structure = ["name", "phone", "address", "suburb", "postcode", "state", "sector", "lat", "lng"]

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/nearby_hospitals_i2", params={"postcode": 3000})
        data = ast.literal_eval(req.text)
        data_structure = list(data[0].keys())

        self.assertEqual(data_structure, expected_structure)


# For Iteration 2 /quiz_i2
class QuizI2(unittest.TestCase):

    # Check the length of response
    def test_response_length(self):
        expected_length = 7

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/quiz_i2")
        data = ast.literal_eval(req.text)
        data_length = len(data)

        self.assertEqual(data_length, expected_length)

    # Check the structure of response
    def test_response_structure(self):
        expected_structure = ["topic", "question", "answer", "explanation", "selection_1", "selection_2"]

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/quiz_i2")
        data = ast.literal_eval(req.text)
        data_structure = list(data[0].keys())

        self.assertEqual(data_structure, expected_structure)


# Main testing app
if __name__ == '__main__':
    unittest.main()