import jwt
from fastapi import Depends, HTTPException, status, FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Define the security scheme (Bearer token)
security = HTTPBearer()

SECRET_KEY = "your_jwt_secret_key4e69f70bc04d8f2d5e7b5bcae4323b72eae4f4f9da6132d5a4b3bb8e33b9986bS256"
ALGORITHM = "HS256"

def authenticate(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalidate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
