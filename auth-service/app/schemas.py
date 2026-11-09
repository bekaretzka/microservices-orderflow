from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CredentialBase(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserRegister(CredentialBase):
    pass

class UserLogin(CredentialBase):
    pass 



class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead