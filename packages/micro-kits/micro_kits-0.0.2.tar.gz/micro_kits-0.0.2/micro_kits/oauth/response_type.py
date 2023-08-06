import typing

from micro_kits.oauth.model import ResponseTypeAuthorizationCodeResponse, AuthorizationCodeResponseTypeRequest, \
    ResponseTypeTokenResponse
from micro_kits.oauth.objects import UserObject
from micro_kits.oauth.storage import ObjectStorage


# class ResponseTypeBase:
#
#     def __init__(self, storage: ObjectStorage):
#         self.storage = storage
#
#     async def validate(self, request: AuthorizationCodeResponseTypeRequest):
#         raise NotImplementedError()
#
#     async def generate_authorization_code_response(self,
#                                                    obj: typing.Optional[AuthObject]) -> AuthorizationCodeResponse:
#         raise NotImplementedError()
#
#     async def generate_token_response(self, obj: AuthObject) -> ResponseTypeTokenResponse:
#         raise NotImplementedError()


class AuthorizationCodeResponseType:

    def __init__(self, storage: ObjectStorage):
        self.storage = storage

    async def get_auth_object(self, request) -> typing.Optional[UserObject]:
        """
        获取待认证的对象实例
        :param request:
        :return:
        """
        # 查询client与user信息
        client = await self.storage.get_client_by_identity(identity=request.client_id)
        user = await self.storage.get_user_by_identity(identity=request.user_id)
        user.client = client
        return user

    async def validate(self, request: AuthorizationCodeResponseTypeRequest) -> typing.Optional[UserObject]:
        """
        对认证请求参数进行校验
        :param request:
        :return:
        """
        user = await self.get_auth_object(request=request)

        if not user.client.check_redirect_uri(redirect_uri=request.redirect_uri):
            raise Exception("validate failed: redirect_uri invalid")

        return user

    async def generate_authorization_code_response(self,
                                                   request: AuthorizationCodeResponseTypeRequest,
                                                   obj: typing.Optional[
                                                       UserObject]) -> ResponseTypeAuthorizationCodeResponse:
        """
        生成授权码并组装返回对象
        :param request:
        :param obj:
        :return:
        """
        code = await self.storage.generate_authorize_code(obj, request.redirect_uri, request.scope)
        return ResponseTypeAuthorizationCodeResponse(
            code=code,
            scope=request.scope.split(';'),
            redirect_uri=request.redirect_uri
        )

    async def generate_token_response(self,
                                      request: AuthorizationCodeResponseTypeRequest,
                                      obj: typing.Optional[UserObject],
                                      extra_claims: typing.Dict = None) -> ResponseTypeTokenResponse:
        """
        生成token并组装返回对象
        :param extra_claims:
        :param request:
        :param obj:
        :return:
        """
        token = await self.storage.generate_token(obj, extra_claims)
        return ResponseTypeTokenResponse(
            token=token,
            scope=request.scope.split(';'),
            redirect_uri=request.redirect_uri
        )
