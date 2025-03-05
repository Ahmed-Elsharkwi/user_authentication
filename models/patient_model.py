""" patient model """
from models.connection import DataBase


class Patient(DataBase):
    """ patient class """
    def __init__(self, data):
        """ initialize patient """
        allowed_attributes = [
            'user_name',
            'password',
            'phone_number',
            'first_name',
            'last_name'
        ]
        for key in data:
            if key in allowed_attributes:
                setattr(self, key, data[key])

        super().__init__()

