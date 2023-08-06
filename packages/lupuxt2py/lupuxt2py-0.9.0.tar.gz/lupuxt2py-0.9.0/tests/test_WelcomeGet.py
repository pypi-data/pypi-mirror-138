# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import os
import unittest

from urllib3_mock import Responses

from lupuxt2py import LupusecSevice

responses = Responses('requests.packages.urllib3')
current_folder = os.path.join(os.path.dirname(__file__))




def get_env_data_as_dict(path: str) -> dict:
    if not os.path.isfile(path):
        return {"host": "", "password": "", "user": ""}
    with open(path, 'r') as f:
        return dict(tuple(line.replace('\n', '').split('=')) for line in f.readlines() if not line.startswith('#'))


class WelcomeGetTest(unittest.TestCase):
    def setUp(self):
        self.lupusec = LupusecSevice(api_url="http://localhost:1080",
                                username="user",
                                password="password")
    @responses.activate
    def test_get_sensors(self):

        with open(current_folder + '/responses/welcomeGet.json') as f:
            test_daten = f.read()
        responses.add('GET', '/action/welcomeGet',
                      body=test_daten, status=200,
                      content_type='application/json')
        self.lupusec.get_system_info()


if __name__ == '__main__':
    unittest.main()
