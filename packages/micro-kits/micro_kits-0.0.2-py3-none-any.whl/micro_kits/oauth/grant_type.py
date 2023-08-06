import typing

from micro_kits.oauth.const import GrantTypeEnum
from micro_kits.oauth.model import GrantTypeTokenResponse, GrantTypeRequest
from micro_kits.oauth.objects import UserObject, ClientObject
from micro_kits.oauth.storage import ObjectStorage


class GrantTypeBase:

    def __init__(self, storage: ObjectStorage):
        self.storage = storage

    async def validate(self, request: GrantTypeRequest) -> typing.Union[UserObject, ClientObject]:
        raise NotImplementedError()

    async def generate_token_response(self, request: GrantTypeRequest,
                                      extra_claims: typing.Dict = None) -> GrantTypeTokenResponse:
        """
            生成token并组装返回对象
            :param extra_claims:
            :param request:
            :return:
        """
        obj = await self.validate(request)
        token = await self.storage.generate_token(obj, extra_claims)
        return GrantTypeTokenResponse(
            token=token
        )


class AuthorizationCodeGrantType(GrantTypeBase):
    """
        Authorization Code grant type class
    """

    async def validate(self, request: GrantTypeRequest) -> typing.Union[UserObject, ClientObject]:
        code = await self.storage.find_authorize_code(code=request.code)

        if code is None:
            raise Exception("无效的授权码")
        # 查询client与user信息
        client = await self.storage.get_client_by_identity(identity=code.client_id)
        user = await self.storage.get_user_by_identity(identity=code.user_id)
        user.client = client
        return user


class PasswordGrantType(GrantTypeBase):
    """
        password grant type class
    """

    async def validate(self, request: GrantTypeRequest) -> typing.Union[UserObject]:
        # 查询user信息
        is_authenticated, user = await self.storage.authenticate_user(username=request.username,
                                                                      password=request.password)
        if not is_authenticated:
            raise Exception("无效的用户认证信息")
        return user


class ClientCredentialsGrantType(GrantTypeBase):
    """
        client_credentials grant type class
    """

    async def validate(self, request: GrantTypeRequest) -> typing.Union[ClientObject]:
        # 查询client信息
        is_authenticated, client = await self.storage.authenticate_client(client_id=request.client_id,
                                                                          secret=request.client_secret)
        if not is_authenticated:
            raise Exception("无效的客户端认证信息")
        return client


class RefreshGrantType(GrantTypeBase):
    """
        refresh_token grant type class
    """

    async def validate(self, request: GrantTypeRequest) -> typing.Union[ClientObject]:
        pass

    async def generate_token_response(self, request: GrantTypeRequest,
                                      extra_claims: typing.Dict = None) -> GrantTypeTokenResponse:
        """
            生成token并组装返回对象
            :param extra_claims:
            :param request:
            :return:
        """
        token = await self.storage.refresh_token(refresh_token=request.refresh_token)
        return GrantTypeTokenResponse(
            token=token
        )


GrantTypes = {
    GrantTypeEnum.AuthorizationCode: AuthorizationCodeGrantType,
    GrantTypeEnum.Password: PasswordGrantType,
    GrantTypeEnum.ClientCredentials: ClientCredentialsGrantType,
    GrantTypeEnum.RefreshToken: RefreshGrantType,
}
