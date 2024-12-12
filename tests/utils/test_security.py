import pytest
from datetime import datetime, timedelta, timezone
import jwt
from unittest.mock import patch

from app.utils.security import (
    hash_password,
    verify_password,
    create_token,
    decode_token,
    SECRET_KEY,
    ALGORITHM,
)


class TestSecurity:
    def test_password_hash_and_verify(self):
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert verify_password(password, hashed)
        assert not verify_password("WrongPassword", hashed)

    @patch("app.utils.security.datetime")
    def test_create_token(self, mock_datetime):
        mock_now = datetime.now(timezone.utc)
        mock_datetime.now.return_value = mock_now

        data = {"user": {"id": 1}}
        token = create_token(data)

        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["user"] == {"id": 1}
        assert decoded["is_refresh"] is False
        assert decoded["exp"] == int((mock_now + timedelta(minutes=15)).timestamp())

    @patch("app.utils.security.datetime")
    def test_create_token_with_custom_expiry(self, mock_datetime):
        mock_now = datetime.now(timezone.utc)
        mock_datetime.now.return_value = mock_now

        data = {"user": {"id": 1}}
        custom_expiry = timedelta(days=7)
        token = create_token(data, expires_delta=custom_expiry)

        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["user"] == {"id": 1}
        assert decoded["is_refresh"] is False
        assert decoded["exp"] == int((mock_now + custom_expiry).timestamp())

    @patch("app.utils.security.datetime")
    def test_create_refresh_token(self, mock_datetime):
        mock_now = datetime.now(timezone.utc)
        mock_datetime.now.return_value = mock_now

        data = {"user": {"id": 1}}
        token = create_token(data, is_refresh=True)

        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["user"] == {"id": 1}
        assert decoded["is_refresh"] is True

    def test_decode_token_success(self):
        data = {"user": {"id": 1}, "exp": int(datetime.now(timezone.utc).timestamp()) + 3600}
        token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

        result = decode_token(token)

        assert result["user"] == {"id": 1}

    def test_decode_token_expired(self):
        data = {"user": {"id": 1}, "exp": int(datetime.now(timezone.utc).timestamp()) - 3600}
        token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

        with pytest.raises(jwt.ExpiredSignatureError):
            decode_token(token)

    def test_decode_token_invalid(self):
        with pytest.raises(jwt.InvalidTokenError):
            decode_token("invalid_token")
