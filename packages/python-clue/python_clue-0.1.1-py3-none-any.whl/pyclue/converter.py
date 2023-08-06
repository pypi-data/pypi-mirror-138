from collections import Iterable
from functools import wraps
from google.protobuf.message import Message


def convert_message_to_dict(obj):
  if isinstance(obj, Iterable):
    value_list = []
    for each in obj:
      if isinstance(each, Message):
        each = convert_message_to_dict(each)
      value_list.append(each)
    return value_list

  if isinstance(obj, Message):
    obj_dict = {}
    for field in obj.DESCRIPTOR.fields:
      value = getattr(obj, field.name)
      if isinstance(value, Message):
        value = convert_message_to_dict(value)
      obj_dict[field.name] = value
    return obj_dict

  return obj


def convert():
  """
  변환 decorator
  추후에 변환 가능 타입을 지정할 수 있게 하기 위해 함수로 지정.
  @convert("dict", "df") 등등
  """
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      return convert_message_to_dict(func(*args, **kwargs))
    return wrapper
  return decorator
