from project.server.log import INFO

import json

from project.tests.base import BaseTestCase
from unittest.mock import patch

from project.server.models import Example
from project.server import db

class TestAllBlueprint(BaseTestCase):
    def test_get_all_gets_all_for_valid_input(self):
        with self.client:
            fieldA = "fieldA"
            fieldB = "fieldB"
            fields = [fieldA, fieldB]
            self.add_example(field=fieldA)
            self.add_example(field=fieldB)

            response = self.client.get(
                '/example/all'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully get all examples.')
            self.assertTrue(data['fields'] == json.dumps(fields))
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def add_example(self, field):
        example_data = json.dumps(dict(
            field=field
        ))
        return self.client.post(
            '/example/add',
            data=example_data,
            content_type='application/json'
        )

    def test_get_all_returns_error_on_exception(self):
        with self.client:
            # force exception
            Example.__table__.drop(db.engine)

            response = self.client.get(
                '/example/all'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Some error occurred. Please try again.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)
