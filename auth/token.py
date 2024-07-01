from pydantic import BaseModel


class AppInstallationToken(BaseModel):
    access_token: str


class UserAccessToken(BaseModel):
    access_token: str
