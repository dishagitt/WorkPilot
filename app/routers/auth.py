from fastapi import APIRouter, Depends, Request
from app.database.schemas.user import UserResponse, UserLogin, UserRegister
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.services.auth_service import register_user, login_user
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["Authentication"])


# registration page render
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request}
    )


@router.post("/register", response_model=UserResponse)
def registration(user_data: UserRegister = Depends(UserRegister.as_form), db: Session = Depends(get_db)):
    register_user(db, user_data)
    response = RedirectResponse(
        url = "/",
        status_code = 303
    )
    return response


# login page render
@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request}
    )


@router.post("/login")
def login(
    user_data: UserLogin = Depends(UserLogin.as_form),
    db: Session = Depends(get_db)
):
    token = login_user(db, user_data)

    response = RedirectResponse(
        url="/dashboard",
        status_code=303
    )

    response.set_cookie(
        key="access_token",
        value=token["access_token"],
        httponly=True,
        path="/"
    )
   
    response.set_cookie(
    key="refresh_token",
    value=token["refresh_token"],
    httponly=True
)

    return response


@router.get("/logout")
def logout():

    response = RedirectResponse(
        url="/",
        status_code=303
    )

    response.delete_cookie(
        key="access_token",
        path="/"
    )

    response.delete_cookie(
        key = "refresh_token",
        path = "/" 
    )

    return response
