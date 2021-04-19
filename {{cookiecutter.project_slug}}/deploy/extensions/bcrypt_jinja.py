from jinja2.ext import Extension
import bcrypt

class BCryptExtension(Extension):
    """Jinja2 extension to hash using bcrypt algo."""

    def __init__(self, environment):
        """Initialize the extension with the given environment."""
        super(BCryptExtension, self).__init__(environment)

        def bcrypt_hash(obj):
            value = str(obj).encode()
            salt = bcrypt.gensalt()
            hashv = bcrypt.hashpw(value, salt)
            return hashv.decode("utf-8")

        environment.filters['bcrypt'] = bcrypt_hash