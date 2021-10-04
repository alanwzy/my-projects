import unittest
import requests
import ast

# For Iteration 1 /uvr_location
class UVLocation(unittest.TestCase):

    # Check the structure of response
    def test_response_structure(self):
        expected_structure = ["postcode", "suburb", "UVR", "max_UVR"]

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/uvr_location", params={"postcode": 3000})
        data = ast.literal_eval(req.text)
        data_structure = list(data.keys())

        self.assertEqual(data_structure, expected_structure)


# For Iteration 1 /uvr_inner_suburbs
class InnerSuburbs(unittest.TestCase):

    # Check the length of response
    def test_response_length(self):
        expected_length = 18

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/uvr_inner_suburbs")
        data = ast.literal_eval(req.text)
        data_length = len(data)

        self.assertEqual(data_length, expected_length)

    # Check the structure of response
    def test_response_structure(self):
        expected_structure = ["postcode", "suburb", "UVR", "max_UVR"]

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/uvr_inner_suburbs")
        data = ast.literal_eval(req.text)
        data_structure = list(data[0].keys())

        self.assertEqual(data_structure, expected_structure)


# For Iteration 1 /uvr_protector
class UVProtector(unittest.TestCase):

    # Check the length of response
    def test_response_length(self):
        minimum_length = 4

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/uvr_protector", params={"uvr": 5})
        data = ast.literal_eval(req.text)
        data_length = len(data)

        self.assertTrue(data_length >= minimum_length)

    # Check the structure of response
    def test_response_structure(self):
        expected_structure = ["type", "hat_type", "forehead", "cheek", "nose", "ear", "chin", "neck"]

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/uvr_protector", params={"uvr": 5})
        data = ast.literal_eval(req.text)
        data_structure = list(data[0].keys())

        self.assertEqual(data_structure, expected_structure)


# Main testing app
if __name__ == '__main__':
    unittest.main()