import re

def user_name_password_check(user_name, password):
    """ check the format of the user_name and the password or the user """
    respond = None

    user_check = re.match(r'^[a-zA-Z0-9]{3,16}$', user_name)
    password_check = re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", password)

    if user_check is None:
        respond = 'Not a valid user_name'

    if password_check is None:
        respond = 'Not a valid password'

    return respond
