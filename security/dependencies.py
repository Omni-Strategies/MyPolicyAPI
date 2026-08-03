from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from security.auth import *

# Swagger Authorize → paste JWT (access_token) as Bearer value
bearer_scheme = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        account_type = payload.get("account_type")

        print(f"[DEBUG] decoded token -> user_id={user_id}, account_type={account_type}")  # TEMP

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"id": user_id, "account_type": account_type}

    except JWTError as e:
        print(f"[DEBUG] JWTError: {e}")  # TEMP
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(*allowed_roles: str):
    """
    Returns a dependency that allows any of `allowed_roles`.
    Admins always pass, regardless of what's listed.
    """
    def role_checker(current_user=Depends(get_current_user)):
        if current_user["account_type"] == "admin":
            return current_user
        if current_user["account_type"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to access this resource"
            )
        return current_user
    return role_checker


# Convenience aliases so your route files don't need to change much
customer_required = require_role("customer")
company_admin_required = require_role("company_admin")
admin_required = require_role("admin")  # only "admin" bypasses in role_checker anyway


def assert_company_owns(company_id, current_user: dict) -> None:
    """Raise 403 unless the JWT subject is this company (admins bypass)."""
    if current_user.get("account_type") == "admin":
        return
    if str(company_id) != str(current_user.get("id")):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this company's resources",
        )