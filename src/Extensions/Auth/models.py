"""
Use these models as references.
It's like interfaces.
"""

from collections import UserDict


class User(UserDict):
    """
    Object that represent current_user, default is anonymous user.
    """
    db_dict = {
        'id': None,
        'verification': False,
        'role': 0,
        'anonymous': True,
    }

    def __init__(self, db_dict=None):
        super().__init__(db_dict)
        if db_dict is not None:
            self.data.update({
                'anonymous': False,
            })

    @property
    def anonymous(self):
        return self.data.get('anonymous', True)

    @property
    def verified(self):
        return self.data.get('verification', True)

    @property
    def role(self):
        return self.data.get('role', True)

    def logout(self):
        return True


class Device(UserDict):
    """
    Object that represent current_device, default is anonymous device.
    """
    db_dict = {
        'jwt_identity': None,
        'anonymous': True,
    }

    def __init__(self, db_dict=None):
        super().__init__(db_dict)
        if db_dict is not None:
            self.data.update({
                'anonymous': False,
            })

    @property
    def anonymous(self):
        return self.data.get('anonymous', True)

    @property
    def jwt_identity(self):
        return self.data.get('jwt_identity', None)

    def logout(self):
        return True
