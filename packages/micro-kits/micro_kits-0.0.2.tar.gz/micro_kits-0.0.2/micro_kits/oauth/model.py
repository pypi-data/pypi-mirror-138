import typing


# --- Response type Request model----
from micro_kits.oauth.const import ResponseTypeEnum, GrantTypeEnum
from micro_kits.oauth.token import AuthorizationCode, Token


class AuthorizationCodeResponseTypeRequest(typing.NamedTuple):
    user_id: str
    client_id: str
    response_type: ResponseTypeEnum
    redirect_uri: typing.Union[str]
    scope: str


# --- Grant type Request model----

class GrantTypeRequest(typing.NamedTuple):
    grant_type: GrantTypeEnum

    # Authorize code 模式参数
    code: str = None

    # client_credentials 模式参数
    client_id: str = None
    client_secret: str = None

    # password 模式参数
    username: str = None
    password: str = None

    # refresh 模式参数
    refresh_token: str = None


# --- Response model----
class ResponseTypeAuthorizationCodeResponse(typing.NamedTuple):
    code: AuthorizationCode
    scope: typing.List[str]
    redirect_uri: typing.Union[str]


class ResponseTypeTokenResponse(typing.NamedTuple):
    token: Token
    scope: typing.List[str]
    redirect_uri: typing.Union[str]


class GrantTypeTokenResponse(typing.NamedTuple):
    token: Token
    # scope: typing.List[str]

