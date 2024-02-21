import secrets
# import logging


# logging.basicConfig(level=logging.INFO, filename="log.log")
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# console = logging.StreamHandler()
# console.setLevel(logging.INFO)

# logger.addHandler(console)


def cookie_gen() -> str:
    """
    Returns:
        uid"""
    uid = secrets.token_urlsafe(32)
    return uid
