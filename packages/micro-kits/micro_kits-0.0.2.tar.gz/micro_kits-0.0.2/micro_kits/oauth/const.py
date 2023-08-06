from enum import Enum


class GrantTypeEnum(str, Enum):
    # 授权码模式
    AuthorizationCode = "authorization_code"
    # 密码认证模式
    Password = "password"
    # 客户端认证模式
    ClientCredentials = "client_credentials"
    # 令牌刷新模式
    RefreshToken = "refresh_token"


class ResponseTypeEnum(str, Enum):
    # 返回Authorization Code
    AuthorizationCode = "authorization_code"
    # 返回Token
    Token = "token"

