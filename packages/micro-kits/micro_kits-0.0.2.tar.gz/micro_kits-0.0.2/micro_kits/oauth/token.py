import typing


class Token(typing.NamedTuple):
    token_type: str
    access_token: str
    refresh_token: str
    expire_in: int


class AuthorizationCode(typing.NamedTuple):
    user_id: str
    client_id: str
    code: str
    expire_in: int
    # redirect_uri: typing.Union[str]
    # scope: typing.List[str]
