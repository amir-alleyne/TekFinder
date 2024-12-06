import requests
import pytest
import time
import subprocess
import json

"""
This is a class responsible for testing the profiles endpoint of the API.
"""
class TestProfiles:
    url = "http://127.0.0.1:4000"
    
    @classmethod
    def setup_class(cls):
        """
        This is the setup method for this testing class, it is responsible for booting up a test server to run tests on.
        """
        # Start the API necessary for the testing by running main.py
        cls.api_process = subprocess.Popen(['python', 'main.py'])

        # Wait for the API to be up
        time.sleep(3)

    @classmethod
    def teardown_class(cls):
        """
        This is the teardown method which terminates the process on which the test server was run on after finishing all tests.
        """
        # Terminate the API process after tests are done
        cls.api_process.terminate()

    def test_api_endpoint(self):
        """
        This is a simple test aimed to confirm if the server is up.
        """
        self.url += "/players/profiles"
        response = requests.get(self.url)
        assert response.status_code == 200

    ############################################# Regular Get Player Profiles #############################################
    def test_incorrect_input(self):
        """
        This is a test where the user has provided an incorrect input.
        """
        self.url += "/players/profiles"
        params = {
            "profile": None
        }
        response = requests.get(self.url, params=params)
        assert json.loads(response.text) == ["Error: Please enter a profile"]

    def test_incorrect_profile_input(self):
        """
        This is a test whee the user has provided with an appropriate input but WRONG profile.
        """
        self.url += "/players/profiles"
        params = {
            "profile": "TEST_ERROR"
        }
        response = requests.get(self.url, params=params)
        assert json.loads(response.text) == ["Error: Please enter a correct profile"]

    def test_correct_input(self):
        """
        This is a test where the user provides with a CORRECT profile, regular search.
        """
        self.url += "/players/profiles"
        params = {
            "profile": "Playmaker"
        }
        response = requests.get(self.url, params=params)
        assert len(json.loads(response.text)) != 0

    def test_correct_input_verbose(self):
        """
        This is a test where the user provides with a CORRECT profile, regular search and added request for verbose.
        """
        self.url += "/players/profiles"
        params = {
            "profile": "Playmaker",
            "verbose": "1"
        }
        response = requests.get(self.url, params=params)
        assert len(json.loads(response.text)[0]) > 2


    ############################################# Custom Get Player Profile #############################################

    def test_incorrect_input_custom(self):
        """
        This is a test where the user has provided an incorrect input for the custom profile endpoint.
        """
        self.url += "/players/profiles/custom"
        params = {
            "profile": None,
            "season": "2021"
        }
        response = requests.get(self.url, params=params)
        print(response.text)
        assert json.loads(response.text) == ["Error: Please enter a profile"]

    def test_incorrect_profile_input_custom(self):
        """
        This is a test where the user had provided an incorrect profile input for the custom profile endpoint.
        """
        self.url += "/players/profiles/custom"
        params = {
            "profile": "TEST_ERROR",
            "pos": "{DF}"
        }
        response = requests.get(self.url, params=params)
        assert json.loads(response.text) == ["Error: Please enter a correct profile"]

    def test_correct_input_custom(self):
        """
        This is a test where the user has provided a CORRECT input for the custom profile endpoint.
        """
        self.url += "/players/profiles/custom"
        params = {
            "profile": "Ball Playing Centreback",
            "season": "2021"
        }
        response = requests.get(self.url, params=params)
        print(response.text)
        assert len(json.loads(response.text)) != 0

    def test_correct_input_verbose_custom(self):
        """
        This is a test where the user provides with a CORRECT profile, custom search and added request for verbose.
        """
        self.url += "/players/profiles/custom"
        params = {
            "profile": "Playmaker",
            "pos": "{DF}",
            "verbose": "1"
        }
        response = requests.get(self.url, params=params)
        assert len(json.loads(response.text)[0]) > 2

    #################################################### Get Weights ####################################################

    def test_incorrect_weights_endpoint(self):
        """
        This is a test where we test the incorrect input for the weights endpoint.
        """
        self.url += "/players/profiles/weights"
        params = {
            "profile": None
        }
        response = requests.get(self.url, params=params)
        assert json.loads(response.text) == ["Error: Please enter a profile"]

    def test_incorrect_weights_profile_endpoint(self):
        """
        This is a test where we test the incorrect profile input for the weights endpoint. 
        """
        self.url += "/players/profiles/weights"
        params = {
            "profile": "TEST_ERROR"
        }
        response = requests.get(self.url, params=params)
        assert json.loads(response.text) == ["Error: Please enter a correct profile"]

    def test_correct_weights_endpoint(self):
        """
        This is a test where we test the CORRECT profile input for the weights endpoint.
        """
        self.url += "/players/profiles/weights"
        params = {
            "profile": "Playmaker"
        }
        response = requests.get(self.url, params=params)
        assert len((response.text)) != 0
        
 #################################################### Get Clubs ####################################################
    def test_incorrect_clubs_endpoint_with_id(self):
        """
        This is a test where we test the INCORRECT club retrieval with an id that does not exist.
        """
        self.url += "/clubs"
        params = {
            "club_id": "5000000"
        }
        response = requests.get(self.url, params=params)
        print(json.loads(response.text))
        assert json.loads(response.text) == {"Error": "No Clubs Found"}

    def test_correct_clubs_endpoint_with_id(self):
        """
        This is a test where we test the CORRECT club retrieval with the club_id.
        """
        self.url += "/clubs"
        params = {
            "club_id": "5"
        }
        response = requests.get(self.url, params=params)
        assert len((response.text)) != 0
    def test_correct_clubs_endpoint_with_league_id(self):
        """
        This is a test where we test the CORRECT clubs retrieval specifying a league_id.
        """
        self.url += "/clubs"
        params = {
            "league_id": "5"
        }
        response = requests.get(self.url, params=params)
        assert len((response.text)) != 0

    def test_correct_clubs_endpoint(self):
        """
        This is a test where we test the CORRECT club retrieval for all clubs.
        """
        self.url += "/clubs"
        params = {
          
        }
        response = requests.get(self.url, params=params)
        assert len((response.text)) != 0




