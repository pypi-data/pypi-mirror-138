import typing

from micro_kits.oauth.objects import UserObject, ClientObject, AuthObject
from micro_kits.oauth.token import Token, AuthorizationCode


class ObjectStorage:
    """
        认证对象存储器
        oauth模块中针对认证对象基本操作的待扩展接口，继承后需实现所有预留方法
    """

    async def get_user_by_identity(self, identity: str) -> typing.Optional[UserObject]:
        """
            根据凭证获取user对象
        :param identity:
        :return:
        """
        ...

    async def get_client_by_identity(self, identity: str) -> typing.Optional[ClientObject]:
        """
            根据凭证获取client对象
        :param identity:
        :return:
        """
        ...

    async def authenticate_user(self, username: str, password: str) -> (bool, typing.Optional[UserObject]):
        """
            用户认证
        :param username:
        :param password:
        :return:
        """
        ...

    async def authenticate_client(self, client_id: str, secret: str) -> (bool, typing.Optional[ClientObject]):
        """
            客户端认证
        :param client_id:
        :param secret:
        :return:
        """
        ...

    async def generate_authorize_code(self, obj: UserObject, redirect_uri: str, scope: str) -> AuthorizationCode:
        """
            生成授权码
        :param obj:
        :param redirect_uri:
        :param scope:
        :return:
        """
        ...

    async def find_authorize_code(self, code: str) -> typing.Union[AuthorizationCode, None]:
        """
            查找授权码
        :param code:
        :return:
        """
        ...

    async def delete_authorize_code(self, code: str) -> None:
        """
            删除授权码
        :param code:
        :return:
        """
        ...

    async def generate_token(self, obj: AuthObject, extra_claims: typing.Dict = None) -> Token:
        """
            生成token
        :param obj:
        :param extra_claims:
        :return:
        """
        ...

    async def refresh_token(self, refresh_token: str) -> Token:
        """
            根据有效refresh token刷新token有效期
        :param refresh_token:
        :return:
        """
        ...

    async def revoke_token(self, token: str):
        """
            注销token
        :param token:
        :return:
        """
        ...

    async def validate_token(self, token: str) -> bool:
        """
            校验token有效性
        :param token:
        :return:
        """
        ...

    async def inspect_token(self, token: str) -> typing.Dict:
        """
            解析token携带信息
        :param token:
        :return:
        """
        ...
