from collections import namedtuple
from grpc import ClientCallDetails


class BaseInterceptor:
  """
  code from
  https://www.programcreek.com/python/?code=googleads%2Fgoogle-ads-python%2Fgoogle-ads-python-master%2Fgoogle%2Fads%2Fgoogle_ads%2Finterceptors%2Fmetadata_interceptor.py
  """
  @classmethod
  def get_client_call_details_instance(
      cls,
      method,
      timeout,
      metadata,
      credentials=None
  ):
    """Initializes an instance of the ClientCallDetails with the given data.

    Args:
        method: A str of the service method being invoked.
        timeout: A float of the request timeout
        metadata: A list of metadata tuples
        credentials: An optional grpc.CallCredentials instance for the RPC

    Returns:
        An instance of _ClientCallDetails that wraps grpc.ClientCallDetails.
    """
    class _ClientCallDetails(
        namedtuple(
            '_ClientCallDetails',
            ('method', 'timeout', 'metadata', 'credentials')
        ),
        ClientCallDetails
    ):
      """Wrapper class for initializing a new ClientCallDetails instance."""
      pass

    return _ClientCallDetails(method, timeout, metadata, credentials)

  def _update_client_call_details_metadata(self, client_call_details, metadata):
    """Updates the client call details with additional metadata.

    Args:
        client_call_details: An instance of grpc.ClientCallDetails.
        metadata: Additional metadata defined by GoogleAdsClient.

    Returns:
        An new instance of grpc.ClientCallDetails with additional metadata
        from the GoogleAdsClient.
    """
    client_call_details = self.get_client_call_details_instance(
        client_call_details.method,
        client_call_details.timeout,
        metadata,
        client_call_details.credentials
    )

    return client_call_details
