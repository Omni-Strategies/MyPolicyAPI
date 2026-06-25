from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from security.auth import *
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")
        account_type = payload.get("account_type")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return {
            "id": user_id,
            "account_type": account_type
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

from fastapi import Depends, HTTPException

def customer_required(
    current_user=Depends(get_current_user)
):
    if current_user["account_type"] not in [
        "customer",
        "admin"
    ]:
        raise HTTPException(
            status_code=403,
            detail="Customer access required"
        )

    return current_user

from fastapi import Depends, HTTPException

def admin_required(
    current_user=Depends(get_current_user)
):
    if current_user["account_type"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user