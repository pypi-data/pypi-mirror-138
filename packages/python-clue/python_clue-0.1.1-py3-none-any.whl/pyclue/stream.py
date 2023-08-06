from collections import deque
from threading import Event, Condition

from pyclue.converter import convert


class Stream:
  """
  Controlls data stream.
  """
  def __init__(self, func, request_type, **kwargs):
    self._stop_event = Event()
    self._request_condition = Condition()
    self._response_condition = Condition()

    self.func = func
    self.request_type = request_type
    self.request_param_dict = kwargs

    self._fetch_num_queue = deque()
    self._result = self.func(self)

  def _create_request(self, fetch_num):
    return self.request_type(
        **self.request_param_dict,
        fetch_num=fetch_num
    )

  def _next(self):
    with self._request_condition:
      while not self._fetch_num_queue and not self._stop_event.is_set():
        self._request_condition.wait()
      if self._fetch_num_queue:
        return self._create_request(self._fetch_num_queue.popleft())
      else:
        raise StopIteration

  def __next__(self):
    return self._next()

  def _add_fetch_num(self, fetch_num):
    with self._request_condition:
      self._fetch_num_queue.append(fetch_num)
      self._request_condition.notify()

  @convert()
  def fetchone(self):
    """
    Fetch one response.
    """
    self._add_fetch_num(1)
    return next(self._result)

  @convert()
  def fetchmany(self, num):
    """
    Fetch multiple responses.

    :param int num:
      Number of responses to fetch.
    """
    self._add_fetch_num(num)

    result = []
    for _ in range(num):
      try:
        result.append(next(self._result))
      except StopIteration:
        # when length of result is less then num
        break
    return result

  @convert()
  def fetchall(self):
    self._add_fetch_num(0)
    return [each for each in self._result]

  def close(self):
    """
    Close stream.
    Cll when no longer uses the stream.
    """
    self._stop_event.set()
    with self._request_condition:
      self._request_condition.notify()
