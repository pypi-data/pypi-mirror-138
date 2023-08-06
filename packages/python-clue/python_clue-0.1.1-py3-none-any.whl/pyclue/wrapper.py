from pyclue.connection import Connection


class CLUE:
  """
  Base CLUE class

  :param string host:
    Host of the MDwalks CLUE Connect server
  :param int port:
    Port of the MDwalks CLUE Connect server
  :param string username:
    Username of the account.
  :param string password:
    Password of the account.
  """
  def __init__(self, host: str, port: int, username: str, password: str) -> None:
    self.host = host
    self.port = port
    self.username = username
    self.password = password

  def connect(self) -> Connection:
    """
    Connect to the CLUE server.
    Exception will be raised when connection failed.  

    :return: Connection object.
    :rtype: Connection
    """
    return Connection(
        self.host,
        self.port,
        self.username,
        self.password
    )
