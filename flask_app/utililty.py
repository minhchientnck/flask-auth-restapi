import shortuuid

def generate_username_suffix():
  return shortuuid.ShortUUID(alphabet='0123456789').random(length=6)
