import hashlib
import hmac


def create_sign(key, data, utc_now):
    if data:
        sorted_data = sorted(data.items())
    else:
        sorted_data = {}

    msg = ''.join(
        str(v) for k, v in sorted_data
        if not isinstance(v, (dict, list, type(None)))
    ) + str(utc_now)

    return hmac.new(key.encode(), msg.encode(), hashlib.sha512).hexdigest()