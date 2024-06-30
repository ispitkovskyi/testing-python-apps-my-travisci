from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as c:
            with self.app_context():
                r = c.post('/register', json={'username': 'test', 'password': '1234'})

                self.assertEqual(r.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual(d1={'message': 'User created successfully.'},
                                     d2=json.loads(r.data))

    def test_register_and_login(self):
        with self.app() as c:
            with self.app_context():
                # here use 'json', because 'data' - sends data in "form" format, which causes error
                c.post('/register', json={'username': 'test', 'password': '1234'})

                # Send request to '/auth' endpoint to receive authentication token
                # here use 'data' to send data in format of "form"
                auth_request = c.post('/auth', data=json.dumps({  # json.dumps() converts dictionary into a JSON string
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'}) # returns an encoded JWT token 'access_token'

                # asserts that 'access_token' member exists in list of json-keys in the response body converted to JSON
                self.assertIn('access_token', json.loads(auth_request.data).keys())
                # Example of json.loads(auth_response.data) output:
                # {'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTUxNzcwNTcsImlhdCI6MTcxNTE3Njc1NywibmJmIjoxNzE1MTc2NzU3LCJpZGVudGl0eSI6MX0.McgOe7CTCossmW2l3gQBaU5IQaJ_fwVP5LX5BgRw_jM'}

    def test_register_duplicate_user(self):
        with self.app() as c:
            with self.app_context():
                c.post('/register', json={'username': 'test', 'password': '1234'})
                r = c.post('/register', json={'username': 'test', 'password': '1234'})

                self.assertEqual(r.status_code, 400)
                self.assertDictEqual(d1={'message': 'A user with that username already exists'},
                                     d2=json.loads(r.data))
