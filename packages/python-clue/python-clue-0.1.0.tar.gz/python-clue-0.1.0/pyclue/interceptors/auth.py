from grpc import (
    UnaryUnaryClientInterceptor,
    UnaryStreamClientInterceptor,
    StreamUnaryClientInterceptor,
    StreamStreamClientInterceptor
)

from pyclue.interceptors.base import BaseInterceptor


class AuthInterceptor(
    BaseInterceptor,
    UnaryUnaryClientInterceptor,
    UnaryStreamClientInterceptor,
    StreamUnaryClientInterceptor,
    StreamStreamClientInterceptor
):
  def __init__(self):
    self.token = None

  def set_token(self, token):
    self.token = token

  def _intercept(self, continuation, client_call_details, request):
    if client_call_details.metadata is None:
      metadata = []
    else:
      metadata = list(client_call_details.metadata)

    if self.token is not None:
      metadata.append(("access_token", self.token))

    client_call_details = self._update_client_call_details_metadata(
        client_call_details,
        metadata
    )
    return continuation(client_call_details, request)

  def intercept_unary_unary(self, continuation, client_call_details, request):
    return self._intercept(continuation, client_call_details, request)

  def intercept_unary_stream(self, continuation, client_call_details, request):
    return self._intercept(continuation, client_call_details, request)

  def intercept_stream_unary(self, continuation, client_call_details, request_iterator):
    return self._intercept(continuation, client_call_details, request_iterator)

  def intercept_stream_stream(self, continuation, client_call_details, request_iterator):
    return self._intercept(continuation, client_call_details, request_iterator)
