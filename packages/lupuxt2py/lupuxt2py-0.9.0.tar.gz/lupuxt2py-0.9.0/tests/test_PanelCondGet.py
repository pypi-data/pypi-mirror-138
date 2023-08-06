# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import os
import unittest

from urllib3_mock import Responses


responses = Responses('requests.packages.urllib3')
current_folder = os.path.join(os.path.dirname(__file__))





def get_env_data_as_dict(path: str) -> dict:
    if not os.path.isfile(path):
        return {"host": "", "password": "", "user": ""}
    with open(path, 'r') as f:
        return dict(tuple(line.replace('\n', '').split('=')) for line in f.readlines() if not line.startswith('#'))


class PanelCondGetTest(unittest.TestCase):

    def setUp(self):
        from lupuxt2py import LupusecSevice
        self.lupusec = LupusecSevice(api_url="http://localhost:1080",
                                username="user",
                                password="password")

    @responses.activate
    def test_get_sensors(self):
        with open(current_folder + '/responses/panelCondGet.json') as f:
            response_body_text = f.read()
        responses.add('GET', '/action/panelCondGet',
                      body=response_body_text, status=200,
                      content_type='application/json')

        panel=self.lupusec.get_alarm_panel()
        self.assertIsNotNone(panel)


if __name__ == '__main__':
    unittest.main()
