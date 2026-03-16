"""JWT authentication service implementation.

This module provides JWT token generation and validation functionality
based on the auth-system.md design specification.
"""

import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
import os


class JWTService:
    """JWT token management service.

    Implements the token generation and validation as specified in
    docs/designs/auth-system.md section 3.2
    """

    def __init__(self, secret_key: str = None, algorithm: str = "HS256"):
        """Initialize JWT service.

        Args:
            secret_key: Secret key for signing tokens. Defaults to env var.
            algorithm: JWT algorithm to use.
        """
        self.secret_key = secret_key or os.getenv("JWT_SECRET_KEY", "dev-secret")
        self.algorithm = algorithm
        self.token_expiry_hours = 24

    def generate_token(self, user_id: str, payload: Dict = None) -> str:
        """Generate a JWT token for the given user.

        Args:
            user_id: User identifier to encode in token.
            payload: Additional claims to include in token.

        Returns:
            Encoded JWT token string.
        """
        now = datetime.utcnow()
        expiry = now + timedelta(hours=self.token_expiry_hours)

        token_payload = {
            "sub": user_id,
            "iat": now.timestamp(),
            "exp": expiry.timestamp(),
            **(payload or {})
        }

        return jwt.encode(token_payload, self.secret_key, algorithm=self.algorithm)

    def validate_token(self, token: str) -> Optional[Dict]:
        """Validate and decode a JWT token.

        Args:
            token: JWT token string to validate.

        Returns:
            Decoded payload if valid, None otherwise.
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
