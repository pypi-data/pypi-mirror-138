from abc import ABCMeta
from typing import Callable, Optional

from grpc import Channel, channel_ready_future, FutureTimeoutError
from authlib.oauth2.rfc6749 import OAuth2Token

from .._grpc.ApiService_pb2_grpc import ApiServiceStub
from innotescus.auth import InnoAuthClient


class InnotescusServiceBase(metaclass=ABCMeta):
    def __init__(self, channel_factory_: Callable[[], Channel], auth_client: InnoAuthClient, api_base_url: str,
                 verify_ssl: bool = True):
        self.channel_factory = channel_factory_
        self.auth_client = auth_client
        self.verify_ssl = verify_ssl
        self.channel: Optional[Channel] = None
        self.upload_url = f'{api_base_url}/api/upload'
        self.upload_annotations_url = f'{api_base_url}/api/upload/annotations'

    @property
    def _token(self) -> OAuth2Token:
        """ Gets the current API token.  If the currently-downloaded token is expired
        or hasn't yet been fetched, an API call will be made.
        """
        return self.auth_client.fetch_access_token()

    def _connect_to_server(self) -> ApiServiceStub:
        """ Blocking call that will make sure the channel connection
        is ready and then build the GRPC api stub.
        :return: the GRPC API Stub
        """
        try:
            if not self.channel:
                self.channel = self.channel_factory()
            channel_ready_future(self.channel).result(timeout=10)
        except FutureTimeoutError:
            raise
        else:
            return ApiServiceStub(self.channel)
