from project.server.log import INFO

import json

from project.tests.base import BaseTestCase

from project.server.models import Example

class TestAddBlueprint(BaseTestCase):
    def test_add_adds_for_valid_input(self):
        with self.client:
            field = "exampleA"
            example_data = json.dumps(dict(
                field=field
            ))
            response = self.client.post(
                '/example/add',
                data=example_data,
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['field'] == field)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_add_informs_when_example_already_exists(self):
        with self.client:
            field = "exampleA"
            example_data = json.dumps(dict(
                field=field
            ))
            self.client.post(
                '/example/add',
                data=example_data,
                content_type='application/json'
            )
            response = self.client.post(
                '/example/add',
                data=example_data,
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Example with field: ' + field + ' already exists.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_add_returns_error_when_exception_occurs(self):
        with self.client:
            response = self.client.post(
                '/example/add',
                data="INVALID JSON $$#@",
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Some error occurred. Please try again.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)
