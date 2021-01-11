import configparser

_CONFIG_FILE = "conf.ini"
_AUTH_SECTION = "auth"
_AUTH_KEY = "access_key_id"
_AUTH_SECRET = "secret_access_key"


def save_config(access_key_id="", secret_access_key=""):
    cf = configparser.ConfigParser()
    cf.read(_CONFIG_FILE)
    if not cf.has_section(_AUTH_SECTION):
        cf.add_section(_AUTH_SECTION)
    cf.set(_AUTH_SECTION, _AUTH_KEY, access_key_id)
    cf.set(_AUTH_SECTION, _AUTH_SECRET, secret_access_key)
    with open(_CONFIG_FILE, "w") as f:
        cf.write(f)


def load_config():
    cf = configparser.ConfigParser()
    cf.read(_CONFIG_FILE)
    if not cf.has_section(_AUTH_SECTION):
        return {}
    if not all([cf.has_option(_AUTH_SECTION, _AUTH_KEY), cf.has_option(_AUTH_SECTION, _AUTH_SECRET)]):
        return {}
    key_value = cf.get(_AUTH_SECTION, _AUTH_KEY)
    secret_value = cf.get(_AUTH_SECTION, _AUTH_SECRET)
    if not key_value or not secret_value:
        return {}
    return {_AUTH_KEY: key_value, _AUTH_SECRET: secret_value}
