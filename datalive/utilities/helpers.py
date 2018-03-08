
class Helpers:
    
    #function to set a unique user password reset key
    @staticmethod
    def unique_reset_token_key(user):
        import os
        import binascii
        import uuid
        return str(user.id) + '-' + str(uuid.uuid4().hex) + str(uuid.uuid4().hex)

