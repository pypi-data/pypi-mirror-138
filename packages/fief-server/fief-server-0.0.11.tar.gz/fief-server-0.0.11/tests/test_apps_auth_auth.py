from typing import Dict, Optional

import httpx
import pytest
from fastapi import status
from furl import furl

from fief.db import AsyncSession
from fief.managers import GrantManager, LoginSessionManager, SessionTokenManager
from fief.settings import settings
from tests.conftest import TenantParams
from tests.data import TestData


@pytest.mark.asyncio
@pytest.mark.account_host
class TestAuthAuthorize:
    @pytest.mark.parametrize(
        "params,error",
        [
            pytest.param(
                {
                    "response_type": "code",
                    "redirect_uri": "https://nantes.city/callback",
                    "scope": "openid",
                },
                "invalid_client",
                id="Missing client_id",
            ),
            pytest.param(
                {
                    "response_type": "code",
                    "client_id": "INVALID_CLIENT_ID",
                    "redirect_uri": "https://nantes.city/callback",
                    "scope": "openid",
                },
                "invalid_client",
                id="Invalid client",
            ),
            pytest.param(
                {
                    "response_type": "code",
                    "client_id": "DEFAULT_TENANT_CLIENT_ID",
                    "scope": "openid",
                },
                "invalid_redirect_uri",
                id="Missing redirect_uri",
            ),
        ],
    )
    async def test_authorize_error(
        self,
        tenant_params: TenantParams,
        test_client_auth: httpx.AsyncClient,
        params: Dict[str, str],
        error: str,
    ):
        response = await test_client_auth.get(
            f"{tenant_params.path_prefix}/authorize", params=params
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        headers = response.headers
        assert headers["X-Fief-Error"] == error

    @pytest.mark.parametrize(
        "params,error",
        [
            pytest.param(
                {
                    "client_id": "DEFAULT_TENANT_CLIENT_ID",
                    "redirect_uri": "https://nantes.city/callback",
                    "scope": "openid",
                },
                "invalid_request",
                id="Missing response_type",
            ),
            pytest.param(
                {
                    "response_type": "magic_wand",
                    "client_id": "DEFAULT_TENANT_CLIENT_ID",
                    "redirect_uri": "https://nantes.city/callback",
                    "scope": "openid",
                },
                "invalid_request",
                id="Invalid response_type",
            ),
            pytest.param(
                {
                    "response_type": "code",
                    "client_id": "DEFAULT_TENANT_CLIENT_ID",
                    "redirect_uri": "https://nantes.city/callback",
                },
                "invalid_request",
                id="Missing scope",
            ),
            pytest.param(
                {
                    "response_type": "code",
                    "client_id": "DEFAULT_TENANT_CLIENT_ID",
                    "redirect_uri": "https://nantes.city/callback",
                    "scope": "user",
                },
                "invalid_scope",
                id="Missing openid scope",
            ),
            pytest.param(
                {
                    "response_type": "code",
                    "client_id": "DEFAULT_TENANT_CLIENT_ID",
                    "redirect_uri": "https://nantes.city/callback",
                    "scope": "openid",
                    "prompt": "INVALID_PROMPT",
                },
                "invalid_request",
                id="Invalid prompt",
            ),
            pytest.param(
                {
                    "response_type": "code",
                    "client_id": "DEFAULT_TENANT_CLIENT_ID",
                    "redirect_uri": "https://nantes.city/callback",
                    "scope": "openid",
                    "prompt": "none",
                },
                "login_required",
                id="None prompt without session",
            ),
            pytest.param(
                {
                    "response_type": "code",
                    "client_id": "DEFAULT_TENANT_CLIENT_ID",
                    "redirect_uri": "https://nantes.city/callback",
                    "scope": "openid",
                    "prompt": "consent",
                },
                "login_required",
                id="Consent prompt without session",
            ),
            pytest.param(
                {
                    "response_type": "code",
                    "client_id": "DEFAULT_TENANT_CLIENT_ID",
                    "redirect_uri": "https://nantes.city/callback",
                    "scope": "openid",
                    "screen": "INVALID_SCREEN",
                },
                "invalid_request",
                id="Invalid screen",
            ),
        ],
    )
    async def test_authorize_redirect_error(
        self,
        tenant_params: TenantParams,
        test_client_auth: httpx.AsyncClient,
        params: Dict[str, str],
        error: str,
    ):
        response = await test_client_auth.get(
            f"{tenant_params.path_prefix}/authorize", params=params
        )

        assert response.status_code == status.HTTP_302_FOUND

        redirect_uri = response.headers["Location"]

        assert redirect_uri.startswith("https://nantes.city/callback")
        parsed_location = furl(redirect_uri)
        assert parsed_location.query.params["error"] == error

    @pytest.mark.parametrize(
        "screen,prompt,session,redirection",
        [
            pytest.param(None, None, False, "/login", id="Default login screen"),
            pytest.param("login", None, False, "/login", id="Login screen"),
            pytest.param("register", None, False, "/register", id="Register screen"),
            pytest.param(None, None, True, "/consent", id="No prompt with session"),
            pytest.param(None, "none", True, "/consent", id="None prompt with session"),
            pytest.param(
                None, "consent", True, "/consent", id="Consent prompt with session"
            ),
            pytest.param(None, "login", True, "/login", id="Login prompt with session"),
        ],
    )
    async def test_valid(
        self,
        screen: Optional[str],
        prompt: Optional[str],
        session: bool,
        redirection: str,
        tenant_params: TenantParams,
        test_client_auth: httpx.AsyncClient,
        account_session: AsyncSession,
    ):
        params = {
            "response_type": "code",
            "client_id": tenant_params.client.client_id,
            "redirect_uri": "https://nantes.city/callback",
            "scope": "openid",
        }
        if screen is not None:
            params["screen"] = screen
        if prompt is not None:
            params["prompt"] = prompt

        cookies = {}
        if session:
            cookies[settings.session_cookie_name] = tenant_params.session_token.token

        response = await test_client_auth.get(
            f"{tenant_params.path_prefix}/authorize", params=params, cookies=cookies
        )

        assert response.status_code == status.HTTP_302_FOUND

        location = response.headers["Location"]
        assert location.endswith(f"{tenant_params.path_prefix}{redirection}")

        login_session_cookie = response.cookies[settings.login_session_cookie_name]
        login_session_manager = LoginSessionManager(account_session)
        login_session = await login_session_manager.get_by_token(login_session_cookie)
        assert login_session is not None


@pytest.mark.asyncio
@pytest.mark.account_host
class TestAuthGetLogin:
    @pytest.mark.parametrize("cookie", [None, "INVALID_LOGIN_SESSION"])
    async def test_invalid_login_session(
        self,
        cookie: Optional[str],
        tenant_params: TenantParams,
        test_client_auth: httpx.AsyncClient,
    ):
        cookies = {}
        if cookie is not None:
            cookies[settings.login_session_cookie_name] = cookie

        response = await test_client_auth.get(
            f"{tenant_params.path_prefix}/login", cookies=cookies
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        headers = response.headers
        assert headers["X-Fief-Error"] == "invalid_session"

    async def test_valid(
        self, test_client_auth: httpx.AsyncClient, test_data: TestData
    ):
        login_session = test_data["login_sessions"]["default"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token

        response = await test_client_auth.get(f"{path_prefix}/login", cookies=cookies)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.account_host
class TestAuthPostLogin:
    @pytest.mark.parametrize("cookie", [None, "INVALID_LOGIN_SESSION"])
    async def test_invalid_login_session(
        self,
        cookie: Optional[str],
        tenant_params: TenantParams,
        test_client_auth: httpx.AsyncClient,
    ):
        cookies = {}
        if cookie is not None:
            cookies[settings.login_session_cookie_name] = cookie

        response = await test_client_auth.post(
            f"{tenant_params.path_prefix}/login", cookies=cookies
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        headers = response.headers
        assert headers["X-Fief-Error"] == "invalid_session"

    async def test_bad_credentials(
        self, test_client_auth: httpx.AsyncClient, test_data: TestData
    ):
        login_session = test_data["login_sessions"]["default"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token

        response = await test_client_auth.post(
            f"{path_prefix}/login",
            data={
                "username": "anne@bretagne.duchy",
                "password": "foo",
            },
            cookies=cookies,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        headers = response.headers
        assert headers["X-Fief-Error"] == "bad_credentials"

    async def test_valid(
        self,
        test_client_auth: httpx.AsyncClient,
        test_data: TestData,
        account_session: AsyncSession,
    ):
        login_session = test_data["login_sessions"]["default"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token

        response = await test_client_auth.post(
            f"{path_prefix}/login",
            data={
                "username": "anne@bretagne.duchy",
                "password": "hermine",
            },
            cookies=cookies,
        )

        assert response.status_code == status.HTTP_302_FOUND

        redirect_uri = response.headers["Location"]
        assert redirect_uri.endswith(f"{path_prefix}/consent")

        session_cookie = response.cookies[settings.session_cookie_name]
        session_token_manager = SessionTokenManager(account_session)
        session_token = await session_token_manager.get_by_token(session_cookie)
        assert session_token is not None

    async def test_valid_with_session(
        self, test_client_auth: httpx.AsyncClient, test_data: TestData
    ):
        login_session = test_data["login_sessions"]["default"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""
        session_token = test_data["session_tokens"]["regular"]

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token
        cookies[settings.session_cookie_name] = session_token.token

        response = await test_client_auth.post(
            f"{path_prefix}/login",
            data={
                "username": "anne@bretagne.duchy",
                "password": "hermine",
            },
            cookies=cookies,
        )

        assert response.status_code == status.HTTP_302_FOUND

        redirect_uri = response.headers["Location"]
        assert redirect_uri.endswith(f"{path_prefix}/consent")

        assert settings.session_cookie_name not in response.cookies


@pytest.mark.asyncio
@pytest.mark.account_host
class TestAuthGetConsent:
    @pytest.mark.parametrize("cookie", [None, "INVALID_LOGIN_SESSION"])
    async def test_invalid_login_session(
        self,
        cookie: Optional[str],
        tenant_params: TenantParams,
        test_client_auth: httpx.AsyncClient,
    ):
        cookies = {}
        if cookie is not None:
            cookies[settings.login_session_cookie_name] = cookie

        response = await test_client_auth.get(
            f"{tenant_params.path_prefix}/consent", cookies=cookies
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        headers = response.headers
        assert headers["X-Fief-Error"] == "invalid_session"

    @pytest.mark.parametrize("cookie", [None, "INVALID_SESSION_TOKEN"])
    async def test_invalid_session_token(
        self,
        cookie: Optional[str],
        test_client_auth: httpx.AsyncClient,
        test_data: TestData,
    ):
        login_session = test_data["login_sessions"]["default"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token
        if cookie is not None:
            cookies[settings.session_cookie_name] = cookie

        response = await test_client_auth.get(f"{path_prefix}/consent", cookies=cookies)

        assert response.status_code == status.HTTP_302_FOUND

        redirect_uri = response.headers["Location"]
        assert redirect_uri.endswith(f"{path_prefix}/login")

    async def test_valid(
        self, test_client_auth: httpx.AsyncClient, test_data: TestData
    ):
        login_session = test_data["login_sessions"]["default"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""
        session_token = test_data["session_tokens"]["regular"]

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token
        cookies[settings.session_cookie_name] = session_token.token

        response = await test_client_auth.get(f"{path_prefix}/consent", cookies=cookies)

        assert response.status_code == status.HTTP_200_OK

    async def test_none_prompt_without_grant(
        self,
        test_client_auth: httpx.AsyncClient,
        test_data: TestData,
        account_session: AsyncSession,
    ):
        login_session = test_data["login_sessions"]["default_none_prompt"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""
        session_token = test_data["session_tokens"]["regular"]

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token
        cookies[settings.session_cookie_name] = session_token.token

        response = await test_client_auth.get(f"{path_prefix}/consent", cookies=cookies)

        assert response.status_code == status.HTTP_302_FOUND

        redirect_uri = response.headers["Location"]
        assert redirect_uri.startswith(login_session.redirect_uri)
        parsed_location = furl(redirect_uri)
        assert parsed_location.query.params["error"] == "consent_required"
        assert parsed_location.query.params["state"] == login_session.state

        login_session_manager = LoginSessionManager(account_session)
        used_login_session = await login_session_manager.get_by_token(
            login_session.token
        )
        assert used_login_session is None

    async def test_granted(
        self,
        test_client_auth: httpx.AsyncClient,
        test_data: TestData,
        account_session: AsyncSession,
    ):
        login_session = test_data["login_sessions"]["granted_default"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""
        session_token = test_data["session_tokens"]["regular"]

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token
        cookies[settings.session_cookie_name] = session_token.token

        response = await test_client_auth.get(f"{path_prefix}/consent", cookies=cookies)

        assert response.status_code == status.HTTP_302_FOUND

        redirect_uri = response.headers["Location"]
        assert redirect_uri.startswith(login_session.redirect_uri)
        parsed_location = furl(redirect_uri)
        assert "code" in parsed_location.query.params
        assert parsed_location.query.params["state"] == login_session.state

        set_cookie_header = response.headers["Set-Cookie"]
        assert set_cookie_header.startswith(f'{settings.login_session_cookie_name}=""')
        assert "Max-Age=0" in set_cookie_header

        login_session_manager = LoginSessionManager(account_session)
        used_login_session = await login_session_manager.get_by_token(
            login_session.token
        )
        assert used_login_session is None

    async def test_granted_larger_scope(
        self, test_client_auth: httpx.AsyncClient, test_data: TestData
    ):
        login_session = test_data["login_sessions"]["granted_default_larger_scope"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""
        session_token = test_data["session_tokens"]["regular"]

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token
        cookies[settings.session_cookie_name] = session_token.token

        response = await test_client_auth.get(f"{path_prefix}/consent", cookies=cookies)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.account_host
class TestAuthPostConsent:
    @pytest.mark.parametrize("cookie", [None, "INVALID_LOGIN_SESSION"])
    async def test_invalid_login_session(
        self,
        cookie: Optional[str],
        tenant_params: TenantParams,
        test_client_auth: httpx.AsyncClient,
    ):
        cookies = {}
        if cookie is not None:
            cookies[settings.login_session_cookie_name] = cookie

        response = await test_client_auth.post(
            f"{tenant_params.path_prefix}/consent",
            cookies=cookies,
            data={"action": "allow"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        headers = response.headers
        assert headers["X-Fief-Error"] == "invalid_session"

    @pytest.mark.parametrize("cookie", [None, "INVALID_SESSION_TOKEN"])
    async def test_invalid_session_token(
        self,
        cookie: Optional[str],
        test_client_auth: httpx.AsyncClient,
        test_data: TestData,
    ):
        login_session = test_data["login_sessions"]["default"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token
        if cookie is not None:
            cookies[settings.session_cookie_name] = cookie

        response = await test_client_auth.post(
            f"{path_prefix}/consent", cookies=cookies, data={"action": "allow"}
        )

        assert response.status_code == status.HTTP_302_FOUND

        redirect_uri = response.headers["Location"]
        assert redirect_uri.endswith(f"{path_prefix}/login")

    @pytest.mark.parametrize("data", [{}, {"action": "INVALID_ACTION"}])
    async def test_invalid_data(
        self,
        data: Dict[str, str],
        test_client_auth: httpx.AsyncClient,
        test_data: TestData,
    ):
        login_session = test_data["login_sessions"]["default"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""
        session_token = test_data["session_tokens"]["regular"]

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token
        cookies[settings.session_cookie_name] = session_token.token

        response = await test_client_auth.post(
            f"{path_prefix}/consent", cookies=cookies, data=data
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        headers = response.headers
        assert headers["X-Fief-Error"] == "invalid_action"

    async def test_allow(
        self,
        test_client_auth: httpx.AsyncClient,
        test_data: TestData,
        account_session: AsyncSession,
    ):
        login_session = test_data["login_sessions"]["default"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""
        session_token = test_data["session_tokens"]["regular"]

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token
        cookies[settings.session_cookie_name] = session_token.token

        response = await test_client_auth.post(
            f"{path_prefix}/consent", cookies=cookies, data={"action": "allow"}
        )

        assert response.status_code == status.HTTP_302_FOUND

        redirect_uri = response.headers["Location"]
        assert redirect_uri.startswith(login_session.redirect_uri)
        parsed_location = furl(redirect_uri)
        assert "code" in parsed_location.query.params
        assert parsed_location.query.params["state"] == login_session.state

        set_cookie_header = response.headers["Set-Cookie"]
        assert set_cookie_header.startswith(f'{settings.login_session_cookie_name}=""')
        assert "Max-Age=0" in set_cookie_header

        login_session_manager = LoginSessionManager(account_session)
        used_login_session = await login_session_manager.get_by_token(
            login_session.token
        )
        assert used_login_session is None

        grant_manager = GrantManager(account_session)
        grant = await grant_manager.get_by_user_and_client(
            session_token.user_id, client.id
        )
        assert grant is not None
        assert grant.scope == login_session.scope

    async def test_deny(
        self,
        test_client_auth: httpx.AsyncClient,
        test_data: TestData,
        account_session: AsyncSession,
    ):
        login_session = test_data["login_sessions"]["default"]
        client = login_session.client
        tenant = client.tenant
        path_prefix = tenant.slug if not tenant.default else ""
        session_token = test_data["session_tokens"]["regular"]

        cookies = {}
        cookies[settings.login_session_cookie_name] = login_session.token
        cookies[settings.session_cookie_name] = session_token.token

        response = await test_client_auth.post(
            f"{path_prefix}/consent", cookies=cookies, data={"action": "deny"}
        )

        assert response.status_code == status.HTTP_302_FOUND

        redirect_uri = response.headers["Location"]
        assert redirect_uri.startswith(login_session.redirect_uri)
        parsed_location = furl(redirect_uri)
        assert parsed_location.query.params["error"] == "access_denied"
        assert parsed_location.query.params["state"] == login_session.state

        set_cookie_header = response.headers["Set-Cookie"]
        assert set_cookie_header.startswith(f'{settings.login_session_cookie_name}=""')
        assert "Max-Age=0" in set_cookie_header

        login_session_manager = LoginSessionManager(account_session)
        used_login_session = await login_session_manager.get_by_token(
            login_session.token
        )
        assert used_login_session is None
