from unittest.mock import MagicMock

import pytest

from fief.models import Account
from fief.services.email import EmailProvider
from fief.tasks.forgot_password import OnAfterForgotPasswordTask
from tests.data import TestData


@pytest.mark.asyncio
class TestTasksOnAfterForgotPassword:
    async def test_send_forgot_password_email(
        self,
        account: Account,
        global_session_manager,
        account_session_manager,
        test_data: TestData,
    ):
        email_provider_mock = MagicMock(spec=EmailProvider)

        on_after_forgot_password = OnAfterForgotPasswordTask(
            global_session_manager, account_session_manager, email_provider_mock
        )

        user = test_data["users"]["regular"]
        await on_after_forgot_password.run(
            str(user.id), str(account.id), "https://bretagne.fief.dev/reset?token=AAA"
        )

        email_provider_mock.send_email.assert_called_once()
