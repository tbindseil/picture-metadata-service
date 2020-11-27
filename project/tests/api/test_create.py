from project.server.log import INFO

import json

from project.tests.base import BaseTestCase

# TODO package... from dwf.clients.auth.model import User
from project.server.dwf.clients.auth.models import User

from project.server.models import Picture

from unittest.mock import patch

class TestCreateBlueprint(BaseTestCase):
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
        self.patcher = patch('project.server.dwf.clients.auth.apis.authenticate')

        mock_authenticate = self.patcher.start()
        # so I'm worried about something here,
        # I'm worried about if the user doesn't match the user in the token
        # what user? the user that makes the request.
        # well how would they have another token?
        # not worried about it. having the authorization header means you can
        # impersonate the user, so its a moot point to check if the user they
        # say they are doesn't match the token.
        def authenticate_side_effect(token):
            if token == self.good_token:
                return self.user
            elif token == self.other_user_token:
                return self.other_user
            else:
                raise Exception("Unauthorized")
        mock_authenticate.side_effect = authenticate_side_effect

    # actually, its part of the auth service to handle no/bad toke.
    # it is up to pms to call with token (from somewhere?? TODO) always,
    # and handle failure accordingly
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
            mock_authenticate.assert_called_with(self.good_token)

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
                '/example/add',
                data="INVALID JSON $$#@",
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
