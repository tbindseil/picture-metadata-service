from project.server.log import INFO

import json

from project.tests.base import BaseTestCase

# TODO package... from dwf.clients.auth.model import User
from dwfclients.auth.models import User
from dwfclients.auth.apis import AuthException

from project.server.models import Picture
from project.server import db

from unittest.mock import patch

class TestCreateBlueprint(BaseTestCase):
    patcher = None
    mock_authenticate = None

    title = "title"
    title_data = json.dumps(dict(
        title=title
    ))

    good_token = "good_token"
    user = User(
        username='user@test.com',
        admin=False
    )
    other_user_token = "other_user_token"
    other_user = User(
        username='other_user@test.com',
        admin=False
    )
    bad_token = "bad_token"

    def setUp(self):
        BaseTestCase.setUp(self)

        # by default, user is logged in, so authorize returns valid token
        self.patcher = patch('dwfclients.auth.apis.authenticate')
        self.mock_authenticate = self.patcher.start()

        def authenticate_side_effect(token):
            if token == self.good_token:
                return self.user
            elif token == self.other_user_token:
                return self.other_user
            else:
                raise AuthException("Unauthorized")
        self.mock_authenticate.side_effect = authenticate_side_effect

    def tearDown(self):
        BaseTestCase.tearDown(self)
        self.patcher.stop()

    def test_create_verifies_authenticated_always(self):
        with self.client:
            response = self.client.post(
                '/picture-metadata/create',
                data=self.title_data,
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + self.good_token
                )
            )
            self.mock_authenticate.assert_called_with(self.good_token)

    def test_create_returns_unauthenticated_when_no_token(self):
        with self.client:
            response = self.client.post(
                '/picture-metadata/create',
                data=self.title_data,
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid auth token.')
            self.assertEqual(response.status_code, 401)

    def test_create_returns_unauthenticated_when_bad_token(self):
        with self.client:
            response = self.client.post(
                '/picture-metadata/create',
                data=self.title_data,
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + self.bad_token
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid auth token.')
            self.assertEqual(response.status_code, 401)

    def test_create_creates_for_valid_input(self):
        with self.client:
            response = self.client.post(
                '/picture-metadata/create',
                data=self.title_data,
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + self.good_token
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully created picture.')
            self.assertTrue(data['title'] == self.title)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_create_informs_when_picture_already_exists_for_user(self):
        with self.client:
            response = self.client.post(
                '/picture-metadata/create',
                data=self.title_data,
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + self.good_token
                )
            )
            response = self.client.post(
                '/picture-metadata/create',
                data=self.title_data,
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + self.good_token
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Picture with title: ' + self.title + ' already exists.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_create_creates_when_picture_already_exists_for_another_user(self):
        with self.client:
            response = self.client.post(
                '/picture-metadata/create',
                data=self.title_data,
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + self.other_user_token
                )
            )
            response = self.client.post(
                '/picture-metadata/create',
                data=self.title_data,
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + self.good_token
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully created picture.')
            self.assertTrue(data['title'] == self.title)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_create_returns_error_when_exception_occurs(self):
        with self.client:
            response = self.client.post(
                '/picture-metadata/create',
                data="DHFSDHFS###$$$",
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + self.good_token
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Some error occurred. Please try again.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)
