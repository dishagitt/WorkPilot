from fastapi import Depends, HTTPException, status, Request, Response
from app.core.security import verify_access_token
from app.services.user_service import get_user_by_id
from app.dependencies.database import get_db
from sqlalchemy.orm import Session
from app.services.auth_service import refresh_access_token
from fastapi.responses import RedirectResponse
from app.routers.auth import logout


# def get_current_user(
#     request: Request,
#     response: Response,
#     db: Session = Depends(get_db)
# ):

#     access_token = request.cookies.get("access_token")

#     if not access_token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated"
#         )

#     payload = verify_access_token(access_token)

#      # access token expired
#     if payload is None:

#         refresh_token = request.cookies.get("refresh_token")

#         # no refresh token
#         if not refresh_token:
#             return logout()

#         try:
#             new_access_token = refresh_access_token(refresh_token)

#             # update browser cookie
#             response.set_cookie(
#                 key="access_token",
#                 value=new_access_token,
#                 httponly=True
#             )

#             payload = verify_access_token(new_access_token)

#         except Exception:
#             # refresh token expired
#             return logout()


#     email, user_id = payload

#     user = get_user_by_id(db, user_id)

#     if not user:
#         return logout()

#     return user



from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
    ):
    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    email, user_id = payload

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user