# Dependencies
######################

# Type setting
######################

# Functions
######################


def _convert_to_list(_param):
  """
  Check the datatype of _param and change to a list if it is not yet a list.
  """
  if type(_param) != list:
    return [_param]
  else:
    return _param