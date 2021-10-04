import unittest
import requests
import ast

# For Iteration 3 /next_5days_i3
class next_5days_i3(unittest.TestCase):

    # Check the structure of response
    def test_response_structure(self):
        expected_structure = ["suburb", 'date','max_uvr','excellent_activites','poor_activites']

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/next_5days_i3", params={"postcode": 3000})
        data = ast.literal_eval(req.text)
        data_structure = list(data[0].keys())

        self.assertEqual(data_structure, expected_structure)


# For Iteration 3 /forecast_1day_i3
class forecast_1day_i3(unittest.TestCase):

    # Check the structure of response
    def test_response_structure(self):
        expected_structure = ['suburb','low_uv','moderate_uv']

        params = {
            'day': "2021-11-13",
            'postcode': 3000
        }
        req = requests.get(url="https://lemonumbrella.azurewebsites.net/forecast_1day_i3", params=params)
        data = ast.literal_eval(req.text)
        data_structure = list(data.keys())

        self.assertEqual(data_structure, expected_structure)


# For Iteration 3 /uvr_inner_suburbs_i3
class uvr_inner_suburbs_i3(unittest.TestCase):

    # Check the length of response
    def test_response_length(self):
        expected_length = 10

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/uvr_inner_suburbs_i3")
        data = ast.literal_eval(req.text)
        data_length = len(data)

        self.assertEqual(data_length, expected_length)

    # Check the structure of response
    def test_response_structure(self):
        expected_structure = ['postcode','suburb','UVR','max_UVR']

        req = requests.get(url="https://lemonumbrella.azurewebsites.net/uvr_inner_suburbs_i3")
        data = ast.literal_eval(req.text)
        data_structure = list(data[0].keys())

        self.assertEqual(data_structure, expected_structure)


# Main testing app
if __name__ == '__main__':
    unittest.main()