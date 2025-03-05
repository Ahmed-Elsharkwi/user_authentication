""" file model """
from models.connection import DataBase


class File(DataBase):
    """ file class """

    def __init__(self, data):
        """ initialize new file """
        allowed_attributes = [
            'phone_number',
            'first_name',
            'last_name',
            'country_code',
            'result_date',
            'selected_lab_test',
            'result_type',
            'file_path',
            'status',
            'doctor_admin_id',
            'patient_id',
            'file_id'
        ]
        
        for key in data:
            if key in allowed_attributes:
                setattr(self, key, data[key])

        super().__init__()
