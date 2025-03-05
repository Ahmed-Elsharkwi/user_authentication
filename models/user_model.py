""" user model """
from models.connection import DataBase


class Doctor_Admin(DataBase):
    """ user class """
    def __init__(self, data):
        """ initialize new Doctor or new Admin """

        allowed_attributes = [
            'user_name',
            'password',
            'role'
        ]


        for key in data:
            if key in allowed_attributes:
                setattr(self, key, data[key])

        super().__init__()

