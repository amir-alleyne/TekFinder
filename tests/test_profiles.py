import requests
import pytest
import time
import subprocess

"""
This is a class responsible for testing the profiles endpoint of the API.
"""
class TestProfiles:
    url = "http://127.0.0.1:4000/players"
    
    @classmethod
    def setup_class(cls):
        # Start the API necessary for the testing by running main.py
        cls.api_process = subprocess.Popen(['python', 'main.py'])

        # Wait for the API to be up
        time.sleep(3)

    @classmethod
    def teardown_class(cls):
        # Terminate the API process after tests are done
        cls.api_process.terminate()

    def test_api_endpoint(self):
        response = requests.get(self.url)
        assert response.status_code == 200



if __name__ == "__main__":

    url = "http://127.0.0.1:5000/players/profiles"

    args = {"profile": "Target Man", "verbose": True}

    request = requests.get(url=url, params=args)

    print(request.status_code)
    print(request.text)

