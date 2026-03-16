"""Authentication middleware for API requests.

This module provides request authentication middleware that validates
JWT tokens as specified in docs/designs/auth-system.md section 3.3
"""

from typing import Callable, Optional
from fastapi import Request, HTTPException, status
from .jwt import JWTService


class AuthMiddleware:
    """Authentication middleware using JWT tokens.

    Validates JWT tokens on incoming requests and attaches user info
    to the request state if authentication is successful.
    """

    def __init__(self, jwt_service: JWTService = None):
        """Initialize auth middleware.

        Args:
            jwt_service: JWT service instance. Creates default if None.
        """
        self.jwt_service = jwt_service or JWTService()

    async def __call__(self, request: Request, call_next: Callable) -> Callable:
        """Process request with authentication.

        Args:
            request: Incoming FastAPI request.
            call_next: Next middleware in chain.

        Returns:
            Response from next middleware.

        Raises:
            HTTPException: If authentication fails.
        """
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return await call_next(request)

        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format"
            )

        token = auth_header.split(" ")[1]
        payload = self.jwt_service.validate_token(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        request.state.user_id = payload.get("sub")
        request.state.user_claims = payload

        return await call_next(request)


def require_auth(request: Request) -> str:
    """Dependency to require authentication on endpoints.

    Args:
        request: FastAPI request object.

    Returns:
        User ID from authenticated request.

    Raises:
        HTTPException: If user is not authenticated.
    """
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user_id
