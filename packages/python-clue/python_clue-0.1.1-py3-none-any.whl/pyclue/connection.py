from grpc import insecure_channel, intercept_channel

from clue_pb2 import RequestLogin
from clue_pb2_grpc import CLUEStub

from pyclue.features import FeatureAdapter
from pyclue.interceptors import AuthInterceptor


class Connection(FeatureAdapter):
  """
  Connection object that handles all feature calls.
  """
  def __init__(self, host, port, username, password):
    self.username = username
    self.password = password

    self.auth = AuthInterceptor()

    channel = insecure_channel(f"{host}:{port}")
    channel = intercept_channel(channel, self.auth)

    self.stub = CLUEStub(channel)
    try:
      token = self.stub.AuthLogin(
          RequestLogin(
              email=username,
              password=password
          )
      )
    except:
      raise ConnectionError("Could not connect to server.")

    if not token.access_token:
      raise ConnectionRefusedError("Invalid username or password.")
    self.auth.set_token(token.access_token)
