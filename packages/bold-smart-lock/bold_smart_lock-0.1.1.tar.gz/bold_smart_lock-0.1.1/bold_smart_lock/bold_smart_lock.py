"""Bold Smart Lock API wrapper"""

import aiohttp

from .const import (
    API_URI,
    REMOTE_ACTIVATION_ENDPOINT,
    EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT,
)

from .auth import Auth


class BoldSmartLock:
    """A Python Abstraction object to Bold Smart Lock"""

    def __init__(self, session: aiohttp.ClientSession):
        """Initialize the Bold Smart Lock object."""

        self._session = session
        self._auth = Auth(session)

    async def authenticate(
        self,
        email: str,
        password: str,
        verification_code: str,
        validation_id: str = None,
    ):
        """Authenticate with account data, validation id and validation code"""

        return await self._auth.authenticate(
            email, password, verification_code, validation_id
        )

    async def get_device_permissions(self):
        """Get the device data and permissions"""

        headers = await self._auth.headers(True)

        async with self._session.get(
            API_URI + EFFECTIVE_DEVICE_PERMISSIONS_ENDPOINT, headers=headers
        ) as response:
            response_text = await response.text()
            return response_text

    async def re_login(self):
        """Re-login / refresh token"""

        return await self._auth.re_login()

    async def remote_activation(self, device_id: int):
        """Activate the device remotely"""

        headers = await self._auth.headers(True)

        async with self._session.post(
            API_URI + REMOTE_ACTIVATION_ENDPOINT.format(device_id), headers=headers
        ) as response:
            response_text = await response.text()
            return response_text

    def set_token(self, token: str):
        """Set the token"""

        self._auth.set_token(token)

    async def verify_email(self, email: str):
        """Request a validation code by e-mail and get a validation_id"""

        return await self._auth.request_validation_id(email)

