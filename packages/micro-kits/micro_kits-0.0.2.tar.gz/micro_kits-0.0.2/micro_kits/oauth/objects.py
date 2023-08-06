import typing
from dataclasses import dataclass


@dataclass
class AuthObject:
    uid: str
    name: str
    scopes: typing.List[str]


@dataclass
class ClientObject(AuthObject):
    secret: str
    redirect_uris: typing.List[str]

    def check_redirect_uri(self, redirect_uri: str) -> bool:
        return redirect_uri in self.redirect_uris


@dataclass
class UserObject(AuthObject):
    username: str
    password_hash: str
    client: typing.Union[ClientObject, None] = None
