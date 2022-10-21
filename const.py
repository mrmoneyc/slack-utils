import logging


class ConstMeta(type):

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise TypeError(f"Can't rebind const ({name})")
        else:
            self.__setattr__(name, value)


class Const(metaclass=ConstMeta):
    # Slack App OAuth Tokens
    USER_TOKEN = "xoxp-xxxxx-ooooo"
    BOT_TOKEN = "xoxb-xxxxx-ooooo"

    # Use user token when set True
    USE_USER_TOKEN = True

    # Wait time (sec) for Slack API call
    REQUEST_DELAY = 1.2

    # Log Verbosity
    LOG_LEVEL = logging.INFO
