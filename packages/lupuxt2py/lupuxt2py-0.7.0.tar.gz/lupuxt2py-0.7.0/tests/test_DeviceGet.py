# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import logging
import os
import unittest

from urllib3_mock import Responses

from lupuxt2py import LupusecSevice

responses = Responses('requests.packages.urllib3')

current_folder = os.path.join(os.path.dirname(__file__))

_LOGGER = logging.getLogger("LupusecSevice")

def get_env_data_as_dict(path: str) -> dict:
    if not os.path.isfile(path):
        return {"host": "", "password": "", "user": ""}
    with open(path, 'r') as f:
        return dict(tuple(line.replace('\n', '').split('=')) for line in f.readlines() if not line.startswith('#'))

data = get_env_data_as_dict("../.env")

class DeviceGetTest(unittest.TestCase):

    @responses.activate
    def test_get_sensors(self):
        lupusec = LupusecSevice(api_url="http://localhost:1080",
                                username="user",
                                password="password")
        with open(current_folder + '/responses/deviceGet.json') as f:
            contents = f.read()
        responses.add('GET', '/action/deviceGet',
                      body=contents, status=200)
        lst=lupusec.get_sensor_list().values()
        flatten = [val for sublist in lst for val in sublist]
        self.assertEqual(flatten.__len__(), 54)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
