import aioredis
import json
import html_to_json

from unittest import IsolatedAsyncioTestCase

from rethinkdb import r

from eyja.main import Eyja
from eyja.utils import render_template

from eyja_email.models import Email

from eyja_fastapi.processes.auth import (
    AuthorizationProcess,
    RegistrationProcess,
)
from eyja_fastapi.models import User, ConfirmToken
from eyja_fastapi.errors import *


class UserAuthorizationTest(IsolatedAsyncioTestCase):
    redis_url = 'redis://localhost:30002/4'

    async def test_authorization_wrong_username_field(self):
        await Eyja.reset()
        await Eyja.init(config_file='tests/config/full_config_without_confirmation.yml')

        await RegistrationProcess.run(
            email='test10@test.com',
            password='passTeSt123'
        )

        with self.assertRaises(MissingRequiredFieldError):
            await AuthorizationProcess.run(
                username='test10@test.com',
                password='passTeSt123'
            )

    async def test_authorization_wrong_user(self):
        await Eyja.reset()
        await Eyja.init(config_file='tests/config/full_config_without_confirmation.yml')

        await RegistrationProcess.run(
            email='test11@test.com',
            password='passTeSt123'
        )

        with self.assertRaises(UserNotFoundError):
            await AuthorizationProcess.run(
                email='test111@test.com',
                password='passTeSt123'
            )

    async def test_authorization_wrong_password(self):
        await Eyja.reset()
        await Eyja.init(config_file='tests/config/full_config_without_confirmation.yml')

        await RegistrationProcess.run(
            email='test12@test.com',
            password='passTeSt123'
        )

        with self.assertRaises(UserNotFoundError):
            await AuthorizationProcess.run(
                email='test12@test.com',
                password='passTeSt1234'
            )

    async def test_authorization_inactive_user(self):
        await Eyja.reset()
        await Eyja.init(config_file='tests/config/full_config.yml')

        await RegistrationProcess.run(
            email='test13@test.com',
            password='passTeSt123'
        )

        with self.assertRaises(UserNotFoundError):
            await AuthorizationProcess.run(
                email='test13@test.com',
                password='passTeSt1234'
            )

    async def test_authorization(self):
        await Eyja.reset()
        await Eyja.init(config_file='tests/config/full_config_without_confirmation.yml')

        user = await RegistrationProcess.run(
            email='test14@test.com',
            password='passTeSt123'
        )

        auth_user, refresh_token, access_token = await AuthorizationProcess.run(
            email='test14@test.com',
            password='passTeSt123',
        )

        self.assertEqual(auth_user.email, user.email)
        self.assertEqual(refresh_token.user_id, user.object_id)
        self.assertEqual(access_token.user_id, user.object_id)
